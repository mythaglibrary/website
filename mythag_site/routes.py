"""Project authored docs into stable public routes for Zensical."""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mythag_site.awakeners import Guide


def _legacy_routes(guides: list[Guide]) -> dict[str, str]:
    from mythag_site.awakeners import KNOWN_REALMS

    routes = {
        "/awakeners": "/handbook/awakeners/",
        "/handbook/awakeners/index": "/handbook/awakeners/",
    }
    for guide in guides:
        routes[f"/awakeners/{guide.slug}"] = f"/handbook/awakeners/{guide.slug}/"
        # Preserve bookmarks even if the authored guide later changes realm.
        for realm in sorted(KNOWN_REALMS):
            routes[f"/handbook/awakeners/{realm}/{guide.slug}"] = f"/handbook/awakeners/{guide.slug}/"
    return routes


def _redirect_page(target: str) -> bytes:
    escaped = html.escape(target, quote=True)
    literal = json.dumps(target).replace("<", "\\u003c")
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="robots" content="noindex">\n'
        f'<link rel="canonical" href="{escaped}">\n'
        f'<meta http-equiv="refresh" content="0; url={escaped}">\n'
        '<title>Page moved</title>\n'
        f'<script>location.replace({literal} + location.search + location.hash);</script>\n'
        f'</head><body><a href="{escaped}">Continue to the guide</a></body></html>\n'
    ).encode("utf-8")


def sync_docs(root: Path, guides: list[Guide]) -> None:
    """Refresh generated-docs without changing sources or touching unchanged files."""
    root = root.resolve()
    source = root / "lib"
    generated = root / "generated-docs"
    # Never follow a substituted output directory outside the workspace.
    if generated.resolve() != generated or generated.is_symlink():
        raise ValueError(f"Generated docs must be a real workspace directory: {generated}")
    generated.mkdir(exist_ok=True)
    expected: set[Path] = set()

    def destination(relative: Path) -> Path:
        path = generated / relative
        if not path.resolve().is_relative_to(generated) or path.is_symlink():
            raise ValueError(f"Generated docs path escapes output directory: {path}")
        expected.add(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def write(relative: Path, content: bytes) -> None:
        path = destination(relative)
        if not path.is_file() or path.read_bytes() != content:
            temporary = path.with_name(f".{path.name}.tmp")
            temporary.write_bytes(content)
            temporary.replace(path)

    routes = _legacy_routes(guides)
    # Match complete root-relative destinations, never a suffix of an external
    # URL or an image path. Query strings and fragments remain outside the match.
    pattern = re.compile(
        r"(?<![\w/:.-])(?:"
        + "|".join(re.escape(route) for route in sorted(routes, key=len, reverse=True))
        + r")/?(?=$|[?#\s\"'<>)\]{}])"
    )
    guide_paths = {
        Path("handbook/awakeners") / guide.realm / f"{guide.slug}.md":
        Path("handbook/awakeners") / f"{guide.slug}.md"
        for guide in guides
    }

    for path in source.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if relative == Path("_redirects"):
            continue
        output = guide_paths.get(relative, relative)
        if path.suffix.lower() == ".md":
            text = path.read_bytes().decode("utf-8")
            text = pattern.sub(lambda match: routes[match.group().rstrip("/")], text)
            write(output, text.encode("utf-8"))
        else:
            target = destination(output)
            original_stat = path.stat()
            target_stat = target.stat() if target.is_file() else None
            if (
                target_stat is None
                or target_stat.st_size != original_stat.st_size
                or target_stat.st_mtime_ns != original_stat.st_mtime_ns
            ):
                temporary = target.with_name(f".{target.name}.tmp")
                shutil.copy2(path, temporary)
                temporary.replace(target)

    redirect_lines = ["# Generated stable Awakener routes"]
    for old, new in routes.items():
        write(Path(old.lstrip("/")) / "index.html", _redirect_page(new))
        redirect_lines.extend((f"{old} {new} 301", f"{old}/ {new} 301"))
    authored_redirects = source / "_redirects"
    redirects = "\n".join(redirect_lines) + "\n"
    if authored_redirects.is_file():
        redirects += "\n" + authored_redirects.read_text(encoding="utf-8")
    write(Path("_redirects"), redirects.encode("utf-8"))

    # Only prune this generated tree, and verify every resolved deletion target.
    for path in sorted(generated.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if not path.resolve().is_relative_to(generated) or path.is_symlink():
            raise ValueError(f"Unsafe generated docs path: {path}")
        if path.is_file() and path not in expected:
            path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()
