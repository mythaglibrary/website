"""Place optional authored guide sections outside the portrait overview."""

from xml.etree import ElementTree as ET

from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from zensical.extensions.context import ContextPreprocessor


class GuideSections(Treeprocessor):
    def run(self, root: ET.Element) -> None:
        context = ContextPreprocessor.from_markdown(self.md)
        if context is None or context.page.meta.get("template") != "awakeners/awakener.html":
            return
        context.page.meta["mythag_how_to_play"] = ""
        children = list(root)
        for start, child in enumerate(children):
            if child.tag != "h2" or "".join(child.itertext()).strip().casefold() != "how to play":
                continue
            end = next((i for i in range(start + 1, len(children)) if children[i].tag == "h2"), len(children))
            root.remove(child)
            if end == start + 1:
                return  # An empty optional heading should not create an empty section.
            section = ET.Element("mythag-how-to-play")
            section.append(child)
            for element in children[start + 1:end]:
                root.remove(element)
                section.append(element)
            root.insert(start, section)
            return


class ExtractGuideSections(Postprocessor):
    def run(self, text: str) -> str:
        context = ContextPreprocessor.from_markdown(self.md)
        if context is None or context.page.meta.get("template") != "awakeners/awakener.html":
            return text
        before, marker, remaining = text.partition("<mythag-how-to-play>")
        if not marker:
            return text
        section, _, after = remaining.partition("</mythag-how-to-play>")
        context.page.meta["mythag_how_to_play"] = section
        return before + after


class GuideSectionsExtension(Extension):
    def extendMarkdown(self, md) -> None:
        # Group only top-level headings, before TOC generation. Extract after
        # serialization and HTML restoration to preserve the normal Markdown pipeline.
        md.treeprocessors.register(GuideSections(md), "mythag_guide_sections", 6)
        md.postprocessors.register(ExtractGuideSections(md), "mythag_guide_sections", 0)


def makeExtension(**kwargs):
    return GuideSectionsExtension(**kwargs)
