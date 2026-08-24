"""Build the site and replace rendered PNG image URLs with cached AVIF assets."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

from PIL import Image, ImageChops, __version__ as PILLOW_VERSION, features

from mythag_site.awakeners import (
    GENERATED_CONFIG,
    AwakenerValidationError,
    prepare_awakeners,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_IMAGES = ROOT / "lib" / "images"
SITE_ROOT = ROOT / "site"
CACHE_ROOT = ROOT / ".avif-cache"
ABBREVIATIONS = ROOT / "includes" / "abbreviations.md"
ENCODER_OPTIONS: dict[str, int | str] = {
    "quality": 70,
    "speed": 6,
    "subsampling": "4:4:4",
}
CACHE_SCHEMA_VERSION = 1
WHEEL_MAX_EDGE = 640
WHEEL_RESAMPLING = Image.Resampling.LANCZOS
PRESERVED_SOURCE_PNGS = frozenset({Path("logo.png")})
BINARY_ARTIFACT_SUFFIXES = frozenset(
    {
        ".avif",
        ".br",
        ".eot",
        ".gif",
        ".gz",
        ".ico",
        ".jpeg",
        ".jpg",
        ".mp3",
        ".mp4",
        ".ogg",
        ".otf",
        ".pdf",
        ".png",
        ".ttf",
        ".wasm",
        ".wav",
        ".webm",
        ".webp",
        ".woff",
        ".woff2",
        ".zip",
    }
)
IMAGE_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
LINK_TAG = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
SOURCE_ATTRIBUTE = re.compile(
    r"(?P<prefix>(?<![-\w])src\s*=\s*)(?P<quote>['\"])(?P<url>[^'\"]+)(?P=quote)",
    re.IGNORECASE,
)
HREF_ATTRIBUTE = re.compile(
    r"(?P<prefix>(?<![-\w])href\s*=\s*)(?P<quote>['\"])(?P<url>[^'\"]+)(?P=quote)",
    re.IGNORECASE,
)
CLASS_ATTRIBUTE = re.compile(
    r"(?<![-\w])class\s*=\s*(?P<quote>['\"])(?P<value>[^'\"]*)(?P=quote)",
    re.IGNORECASE,
)
WIDTH_ATTRIBUTE = re.compile(
    r"(?<![-\w])width\s*=\s*(?P<quote>['\"])(?P<value>[^'\"]*)(?P=quote)",
    re.IGNORECASE,
)
HEIGHT_ATTRIBUTE = re.compile(
    r"(?<![-\w])height\s*=\s*(?P<quote>['\"])(?P<value>[^'\"]*)(?P=quote)",
    re.IGNORECASE,
)
ABBREVIATION_DEFINITION = re.compile(
    r"^\*\[(?P<term>[^]]+)]\s*:\s*(?P<title>.+)$"
)
ABBREVIATION_SKIP_TAGS = {"abbr", "code", "pre", "script", "style"}


def atomic_write_text(
    destination: Path,
    content: str,
    *,
    encoding: str = "utf-8",
    newline: str | None = "",
) -> None:
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(content, encoding=encoding, newline=newline)
    temporary.replace(destination)


def is_wheel(source: Path) -> bool:
    try:
        relative = source.resolve().relative_to(SOURCE_IMAGES.resolve())
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0].lower() == "wheels"


def source_digest(source: Path) -> str:
    policy: dict[str, object] = {
        "cache_schema": CACHE_SCHEMA_VERSION,
        "format": "AVIF",
        "pillow": PILLOW_VERSION,
        "libavif": features.version("avif") or "unknown",
        **ENCODER_OPTIONS,
    }
    if is_wheel(source):
        policy["resize"] = {
            "max_edge": WHEEL_MAX_EDGE,
            "resampling": WHEEL_RESAMPLING.name,
        }
    serialized_policy = json.dumps(
        policy, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    digest = hashlib.sha256(serialized_policy + b"\0")
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_valid_avif(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            if image.format != "AVIF":
                return False
            image.load()
            return image.width > 0 and image.height > 0
    except (OSError, ValueError):
        return False


def encode_cached(source: Path, cached: Path) -> bool:
    """Create or reuse an AVIF cache entry. Return True when it was encoded."""
    digest = source_digest(source)
    digest_file = cached.with_suffix(".avif.sha256")
    if cached.is_file() and digest_file.is_file():
        try:
            digest_matches = digest_file.read_text(encoding="ascii").strip() == digest
        except (OSError, UnicodeError):
            digest_matches = False
        if digest_matches and is_valid_avif(cached):
            return False

    cached.parent.mkdir(parents=True, exist_ok=True)
    temporary = cached.with_suffix(".tmp.avif")
    try:
        with Image.open(source) as original:
            with original.copy() as delivery:
                if is_wheel(source):
                    delivery.thumbnail(
                        (WHEEL_MAX_EDGE, WHEEL_MAX_EDGE), WHEEL_RESAMPLING
                    )
                size = delivery.size
                original_alpha = delivery.convert("RGBA").getchannel("A").copy()
                delivery.save(
                    temporary,
                    "AVIF",
                    **ENCODER_OPTIONS,
                )

        with Image.open(temporary) as converted:
            if converted.size != size:
                raise RuntimeError(f"AVIF dimensions changed for {source}")
            converted_alpha = converted.convert("RGBA").getchannel("A")
            alpha_error = ImageChops.difference(
                original_alpha, converted_alpha
            ).getextrema()[1]
            if alpha_error > 32:
                raise RuntimeError(
                    f"AVIF alpha error {alpha_error}/255 exceeded 32/255 for {source}"
                )

        temporary.replace(cached)
        atomic_write_text(digest_file, f"{digest}\n", encoding="ascii", newline="\n")
    finally:
        temporary.unlink(missing_ok=True)
    return True


def generate_avif_assets() -> tuple[int, int, int, int]:
    encoded = 0
    reused = 0
    png_bytes = 0
    avif_bytes = 0

    for source in sorted(SOURCE_IMAGES.rglob("*.png")):
        relative = source.relative_to(SOURCE_IMAGES).with_suffix(".avif")
        cached = CACHE_ROOT / relative
        destination = SITE_ROOT / "images" / relative
        if encode_cached(source, cached):
            encoded += 1
        else:
            reused += 1
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached, destination)
        png_bytes += source.stat().st_size
        avif_bytes += cached.stat().st_size

    return encoded, reused, png_bytes, avif_bytes


def local_png(url: str, html_file: Path) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path.lower().endswith(".png"):
        return None

    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        png_file = SITE_ROOT / decoded_path.lstrip("/")
    else:
        png_file = html_file.parent / decoded_path

    try:
        png_file.resolve().relative_to(SITE_ROOT.resolve())
    except ValueError:
        return None

    if not png_file.with_suffix(".avif").is_file():
        return None

    return png_file


def avif_url(url: str, html_file: Path) -> str | None:
    if local_png(url, html_file) is None:
        return None

    parsed = urlsplit(url)
    avif_path = f"{parsed.path[:-4]}.avif"
    return urlunsplit(("", "", avif_path, parsed.query, parsed.fragment))


@lru_cache(maxsize=None)
def image_size(source: Path) -> tuple[int, int]:
    with Image.open(source) as image:
        return image.size


def add_intrinsic_dimensions(tag: str, source: Path) -> str:
    width_match = WIDTH_ATTRIBUTE.search(tag)
    height_match = HEIGHT_ATTRIBUTE.search(tag)
    if width_match and height_match:
        return tag

    source_width, source_height = image_size(source)

    if width_match:
        try:
            width = float(width_match.group("value"))
        except ValueError:
            return tag
        height = round(source_height * width / source_width)
        attributes = f' height="{height}"'
    elif height_match:
        try:
            height = float(height_match.group("value"))
        except ValueError:
            return tag
        width = round(source_width * height / source_height)
        attributes = f' width="{width}"'
    else:
        attributes = f' width="{source_width}" height="{source_height}"'

    insert_at = tag.rfind("/>")
    if insert_at == -1:
        insert_at = tag.rfind(">")
    return f"{tag[:insert_at]}{attributes}{tag[insert_at:]}"


def rewrite_html_images() -> tuple[int, int]:
    changed_files = 0
    changed_urls = 0

    for html_file in sorted(SITE_ROOT.rglob("*.html")):
        html = html_file.read_text(encoding="utf-8")
        replacements = 0

        def replace_tag(tag_match: re.Match[str]) -> str:
            nonlocal replacements
            tag = tag_match.group(0)
            source_match = SOURCE_ATTRIBUTE.search(tag)
            if source_match is None:
                return tag

            source = local_png(source_match.group("url"), html_file)
            replacement = avif_url(source_match.group("url"), html_file)
            if replacement is None:
                return tag

            rewritten_tag = SOURCE_ATTRIBUTE.sub(
                lambda match: (
                    f'{match.group("prefix")}{match.group("quote")}'
                    f'{replacement}{match.group("quote")}'
                ),
                tag,
                count=1,
            )
            replacements += 1
            assert source is not None
            return add_intrinsic_dimensions(rewritten_tag, source.with_suffix(".avif"))

        def replace_glightbox_link(tag_match: re.Match[str]) -> str:
            nonlocal replacements
            tag = tag_match.group(0)
            class_match = CLASS_ATTRIBUTE.search(tag)
            if class_match is None or "glightbox" not in class_match.group("value").split():
                return tag
            href_match = HREF_ATTRIBUTE.search(tag)
            if href_match is None:
                return tag
            replacement = avif_url(href_match.group("url"), html_file)
            if replacement is None:
                return tag
            replacements += 1
            return HREF_ATTRIBUTE.sub(
                lambda match: (
                    f'{match.group("prefix")}{match.group("quote")}'
                    f'{replacement}{match.group("quote")}'
                ),
                tag,
                count=1,
            )

        rewritten = IMAGE_TAG.sub(replace_tag, html)
        rewritten = LINK_TAG.sub(replace_glightbox_link, rewritten)
        if replacements:
            atomic_write_text(html_file, rewritten)
            changed_files += 1
            changed_urls += replacements

    return changed_files, changed_urls


def load_abbreviations() -> dict[str, str]:
    definitions: dict[str, str] = {}
    for line_number, line in enumerate(
        ABBREVIATIONS.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.startswith("*["):
            continue
        match = ABBREVIATION_DEFINITION.fullmatch(line)
        if match is None:
            raise RuntimeError(
                f"Invalid abbreviation definition at {ABBREVIATIONS}:{line_number}"
            )
        term = match.group("term").strip()
        title = match.group("title").strip()
        if not term or not title:
            raise RuntimeError(
                f"Empty abbreviation definition at {ABBREVIATIONS}:{line_number}"
            )
        if term in definitions:
            raise RuntimeError(
                f"Duplicate abbreviation {term!r} at {ABBREVIATIONS}:{line_number}"
            )
        definitions[term] = title
    if not definitions:
        raise RuntimeError(f"No abbreviation definitions found in {ABBREVIATIONS}")
    return definitions


class AwakenerAbbreviationParser(HTMLParser):
    def __init__(self, definitions: dict[str, str]) -> None:
        super().__init__(convert_charrefs=False)
        terms = sorted(definitions, key=len, reverse=True)
        self.pattern = re.compile(
            rf"\b(?:{'|'.join(re.escape(term) for term in terms)})\b"
        )
        self.definitions = definitions
        self.output: list[str] = []
        self.replacements = 0
        self._scope_tag: str | None = None
        self._scope_depth = 0
        self._skip_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.output.append(self.get_starttag_text())
        attributes = dict(attrs)
        if self._scope_tag is not None:
            if tag == self._scope_tag:
                self._scope_depth += 1
            if tag in ABBREVIATION_SKIP_TAGS:
                self._skip_depth += 1
        elif "data-abbreviations" in attributes:
            self._scope_tag = tag
            self._scope_depth = 1

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        self.output.append(f"</{tag}>")
        if self._scope_tag is None:
            return
        if tag in ABBREVIATION_SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        if tag == self._scope_tag:
            self._scope_depth -= 1
            if not self._scope_depth:
                self._scope_tag = None

    def handle_data(self, data: str) -> None:
        if self._scope_tag is None or self._skip_depth:
            self.output.append(data)
            return

        def replace(match: re.Match[str]) -> str:
            self.replacements += 1
            term = match.group(0)
            title = html.escape(self.definitions[term], quote=True)
            return f'<abbr title="{title}">{html.escape(term)}</abbr>'

        self.output.append(self.pattern.sub(replace, data))

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self.output.append(f"<?{data}>")

    def unknown_decl(self, data: str) -> None:
        self.output.append(f"<![{data}]>")


def expand_html_abbreviations(
    definitions: dict[str, str] | None = None,
) -> tuple[int, int]:
    if definitions is None:
        definitions = load_abbreviations()
    changed_files = 0
    changed_terms = 0
    for html_file in sorted(SITE_ROOT.rglob("*.html")):
        source = html_file.read_text(encoding="utf-8")
        parser = AwakenerAbbreviationParser(definitions)
        parser.feed(source)
        parser.close()
        if not parser.replacements:
            continue
        atomic_write_text(html_file, "".join(parser.output))
        changed_files += 1
        changed_terms += parser.replacements
    return changed_files, changed_terms


def source_png_candidates() -> list[tuple[Path, Path, Path]]:
    candidates: list[tuple[Path, Path, Path]] = []
    for source in sorted(SOURCE_IMAGES.rglob("*.png")):
        relative = source.relative_to(SOURCE_IMAGES)
        if relative in PRESERVED_SOURCE_PNGS:
            continue
        built_png = SITE_ROOT / "images" / relative
        candidates.append((relative, built_png, built_png.with_suffix(".avif")))
    return candidates


def _normalized_artifact_text(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        relative = path.relative_to(SITE_ROOT).as_posix()
        raise RuntimeError(f"Cannot inspect deployable artifact {relative} as UTF-8") from error
    normalized = unquote(html.unescape(source)).casefold()
    return normalized.replace("\\u002e", ".").replace("\\/", "/")


def verify_and_prune_source_pngs() -> tuple[int, int]:
    candidates = source_png_candidates()
    failures: list[str] = []
    for relative, built_png, built_avif in candidates:
        if not built_png.is_file():
            failures.append(f"missing built PNG images/{relative.as_posix()}")
        if not is_valid_avif(built_avif):
            avif_path = relative.with_suffix(".avif").as_posix()
            failures.append(f"missing or invalid AVIF images/{avif_path}")

    allowed_png_references = tuple(
        f"images/{relative.as_posix()}".casefold()
        for relative in PRESERVED_SOURCE_PNGS
    )
    for artifact in sorted(path for path in SITE_ROOT.rglob("*") if path.is_file()):
        if artifact.suffix.casefold() in BINARY_ARTIFACT_SUFFIXES:
            continue
        text = _normalized_artifact_text(artifact)
        for allowed_reference in allowed_png_references:
            text = text.replace(allowed_reference, "")
        if ".png" in text:
            failures.append(
                f"{artifact.relative_to(SITE_ROOT).as_posix()} contains an "
                "unexpected PNG reference"
            )

    if failures:
        details = "\n".join(f"- {failure}" for failure in failures[:20])
        if len(failures) > 20:
            details += f"\n- ... and {len(failures) - 20} more"
        raise RuntimeError(f"Refusing to prune source PNGs:\n{details}")

    pruned_bytes = sum(built_png.stat().st_size for _, built_png, _ in candidates)
    for _, built_png, _ in candidates:
        built_png.unlink()
    return len(candidates), pruned_bytes


def main() -> None:
    if not features.check("avif"):
        raise SystemExit("Pillow was installed without AVIF support")

    try:
        guides = prepare_awakeners()
    except AwakenerValidationError as error:
        raise SystemExit(str(error)) from error

    definitions = load_abbreviations()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "zensical",
            "build",
            "--clean",
            "--config-file",
            str(GENERATED_CONFIG),
        ],
        cwd=ROOT,
        check=True,
    )
    encoded, reused, png_bytes, avif_bytes = generate_avif_assets()
    changed_files, changed_urls = rewrite_html_images()
    abbreviation_files, abbreviation_terms = expand_html_abbreviations(definitions)
    pruned_files, pruned_bytes = verify_and_prune_source_pngs()
    reduction = (1 - avif_bytes / png_bytes) * 100 if png_bytes else 0
    print(
        f"Awakener content: {len(guides)} guides valid\n"
        "AVIF delivery: "
        f"{encoded} encoded, {reused} cached, {changed_urls} image URLs across "
        f"{changed_files} HTML files, {reduction:.1f}% fewer image bytes\n"
        "Awakener abbreviations: "
        f"{abbreviation_terms} terms across {abbreviation_files} HTML files\n"
        "PNG pruning: "
        f"{pruned_files} redundant files, {pruned_bytes / 1024 / 1024:.1f} MiB removed"
    )


if __name__ == "__main__":
    main()
