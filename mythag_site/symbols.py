"""Author-maintained inline icon shortcuts for Markdown and template prose."""

from __future__ import annotations

import difflib
import re
from functools import lru_cache
from pathlib import Path
from xml.etree import ElementTree as ET

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import AtomicString

from mythag_site.content import ROOT, load_yaml

TOKEN = re.compile(r"(?<![\w:/]):([a-z][a-z0-9_-]*):(?![\w/])")
URL = re.compile(r"(?:https?://|mailto:|/)[^\s<>]+")


class SymbolValidationError(ValueError):
    """Invalid symbol definitions or an unknown authored shortcut."""


def load_symbols(root: Path = ROOT) -> dict[str, dict[str, str | int]]:
    path = root / "content" / "symbols.yaml"
    if not path.exists():
        return {}
    try:
        registry = load_yaml(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SymbolValidationError(f"{path}: {exc}") from exc
    if not isinstance(registry, dict):
        raise SymbolValidationError(f"{path}: expected a mapping of symbol names")
    for name, entry in registry.items():
        location = f"{path}: {name}"
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_-]*", name):
            raise SymbolValidationError(f"{location}: expected a lowercase symbol name")
        if name in _emoji_names():
            raise SymbolValidationError(f"{location}: name is reserved by a built-in emoji; choose another symbol name")
        if not isinstance(entry, dict) or set(entry) - {"label", "icon", "light_icon", "description", "width"}:
            raise SymbolValidationError(f"{location}: expected label, icon, optional light_icon, description and width")
        for field in ("label", "icon", *[key for key in ("light_icon", "description") if key in entry]):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise SymbolValidationError(f"{location}.{field}: expected a non-empty string")
        if "width" in entry and (type(entry["width"]) is not int or entry["width"] <= 0):
            raise SymbolValidationError(f"{location}.width: expected a positive integer pixel width")
        for field in ("icon", "light_icon"):
            if field not in entry:
                continue
            value = entry[field]
            asset = (root / "lib" / value.lstrip("/")).resolve()
            if not value.startswith("/images/") or not asset.is_relative_to((root / "lib" / "images").resolve()) or not asset.is_file():
                raise SymbolValidationError(f"{location}.{field}: expected an existing local /images/ asset")
    return registry


@lru_cache(maxsize=1)
def _emoji_names() -> set[str]:
    # Use the site's own emoji index, including its Material icon aliases.
    from zensical.extensions.emoji import twemoji

    index = twemoji({}, None)
    return {name.strip(":") for key in ("emoji", "aliases") for name in index[key]}


def _element(entry: dict[str, str | int]) -> ET.Element:
    wrapper = ET.Element("span", {"class": "mythag-symbol"})
    if "width" in entry:
        wrapper.set("class", "mythag-symbol mythag-symbol--sized")
        wrapper.set("style", f"--mythag-symbol-width: {entry['width']}px")
    if entry.get("description"):
        wrapper.set("title", entry["description"])
    for field in ("icon", "light_icon"):
        if field not in entry:
            continue
        source = entry[field]
        if "light_icon" in entry:
            source += "#only-dark" if field == "icon" else "#only-light"
        ET.SubElement(wrapper, "img", {
            "src": source, "alt": entry["label"], "loading": "lazy",
        })
    return wrapper


class SymbolTreeprocessor(Treeprocessor):
    def __init__(self, md: Markdown, registry: dict[str, dict[str, str | int]]):
        super().__init__(md)
        self.registry = registry

    def _parts(self, text: str | None) -> list[str | ET.Element]:
        if not text or isinstance(text, AtomicString):
            return [text or ""]
        # Raw inline HTML is stashed by Markdown. Preserve the entire text
        # segment containing it, including contents between its opening/closing tags.
        if "\x02wzxhzdk:" in text:
            return [text]
        urls = list(URL.finditer(text))
        parts: list[str | ET.Element] = []
        cursor = 0
        for match in TOKEN.finditer(text):
            if any(url.start() <= match.start() < url.end() for url in urls):
                continue
            name = match[1]
            if name not in self.registry:
                if name in _emoji_names():
                    continue
                suggestions = difflib.get_close_matches(name, self.registry, n=1)
                hint = f"; did you mean :{suggestions[0]}:?" if suggestions else ""
                raise SymbolValidationError(
                    f"unknown symbol :{name}:{hint}; add it to content/symbols.yaml "
                    "or put literal examples in backticks"
                )
            parts.extend([text[cursor:match.start()], _element(self.registry[name])])
            cursor = match.end()
        parts.append(text[cursor:])
        return parts

    def run(self, root: ET.Element) -> None:
        def visit(node: ET.Element) -> None:
            if node.tag in {"code", "pre", "script", "style", "a"}:
                return
            children = list(node)
            for child in children:
                visit(child)
            for owner in [None, *children]:
                parts = self._parts(node.text if owner is None else owner.tail)
                if owner is None:
                    node.text = str(parts[0])
                    position = 0
                else:
                    owner.tail = str(parts[0])
                    position = list(node).index(owner) + 1
                previous = owner
                for part in parts[1:]:
                    if isinstance(part, str):
                        if previous is None:
                            node.text = (node.text or "") + part
                        else:
                            previous.tail = (previous.tail or "") + part
                    else:
                        node.insert(position, part)
                        position += 1
                        previous = part
        visit(root)


def render_metadata_symbols(value: object, root: Path = ROOT) -> dict[str, str]:
    """Gather symbol-bearing prose without changing source metadata values."""
    rendered: dict[str, str] = {}
    def visit(item: object) -> None:
        if isinstance(item, str) and TOKEN.search(item):
            rendered[item] = render_text_symbols(item, root)
        elif isinstance(item, dict):
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)
    visit(value)
    return rendered


class SymbolMetadataPreprocessor(Preprocessor):
    def __init__(self, md: Markdown, root: Path):
        super().__init__(md)
        self.root = root

    def run(self, lines: list[str]) -> list[str]:
        from zensical.extensions.context import ContextPreprocessor

        context = ContextPreprocessor.from_markdown(self.md)
        if context is not None:
            try:
                context.page.meta["mythag_symbols"] = render_metadata_symbols(
                    context.page.meta.get("awakener", {}), self.root
                )
            except SymbolValidationError as exc:
                raise SymbolValidationError(f"{context.page.path}: {exc}") from exc
        return lines


class SymbolsExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {"root": [str(ROOT), "Project root containing content/symbols.yaml"]}
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        root = Path(self.getConfig("root"))
        registry = load_symbols(root)
        md.preprocessors.register(SymbolMetadataPreprocessor(md, root), "mythag_symbol_metadata", 28)
        md.treeprocessors.register(SymbolTreeprocessor(md, registry), "mythag_symbols", 15)


def render_text_symbols(text: str, root: Path = ROOT) -> str:
    """Render a template's plain-text field safely, allowing symbol shortcuts."""
    md = Markdown()
    tree = ET.Element("span")
    tree.text = text
    SymbolTreeprocessor(md, load_symbols(root)).run(tree)
    result = ET.tostring(tree, encoding="unicode", method="html")
    return result[len("<span>"):-len("</span>")]


def validate_symbol_documents(markdown_roots: tuple[Path, ...], root: Path = ROOT) -> None:
    """Check authored symbols in prose and guide fields without building the site."""
    from mythag_site.awakeners import FRONT_MATTER

    for markdown_root in markdown_roots:
        for path in sorted(markdown_root.rglob("*.md")):
            source = path.read_text(encoding="utf-8")
            front = FRONT_MATTER.match(source)
            try:
                if front:
                    meta = load_yaml(front.group("yaml"))
                    if isinstance(meta, dict):
                        render_metadata_symbols(meta.get("awakener", {}), root=root)
                    source = source[front.end():]
                Markdown(extensions=[
                    "pymdownx.superfences", "pymdownx.inlinehilite",
                    "attr_list", "md_in_html", "tables",
                    SymbolsExtension(root=str(root)),
                ]).convert(source)
            except SymbolValidationError as error:
                raise SystemExit(f"{path.relative_to(root)}: {error}") from error


def makeExtension(**kwargs):
    return SymbolsExtension(**kwargs)
