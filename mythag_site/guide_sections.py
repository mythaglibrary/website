"""Expose guide sections to Markdown navigation and the shared page layout."""

import re
from xml.etree import ElementTree as ET

from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from zensical.extensions.context import ContextPreprocessor

SECTION_PATTERN = re.compile(r"<mythag-guide-section>(.*?)</mythag-guide-section>", re.S)
TEMPLATE_TOC_PATTERN = re.compile(r"<mythag-template-toc>.*?</mythag-template-toc>", re.S)


class GuideSections(Treeprocessor):
    def run(self, root: ET.Element) -> None:
        context = ContextPreprocessor.from_markdown(self.md)
        if context is None or context.page.meta.get("template") != "awakeners/awakener.html":
            return
        context.page.meta["mythag_guide_sections"] = []
        children = list(root)
        sections = []
        for start, child in enumerate(children):
            if child.tag != "h2":
                continue
            end = next((i for i in range(start + 1, len(children)) if children[i].tag == "h2"), len(children))
            root.remove(child)
            if end == start + 1:
                continue  # Empty optional sections should not appear in the page or TOC.
            section = ET.Element("mythag-guide-section")
            section.append(child)
            for element in children[start + 1:end]:
                root.remove(element)
                section.append(element)
            sections.append(section)
        # Match the rendered order: overview, authored sections, then builds.
        root.extend(sections)

        # These headings are rendered by Jinja after Markdown. Let the normal
        # TOC processor see them, then remove these temporary copies from prose.
        guide = context.page.meta.get("awakener", {})
        headings = [(f"build-{i}", build["name"]) for i, build in enumerate(guide.get("builds", []), 1)]
        if guide.get("suggested_posses") or guide.get("suggested_posses_note"):
            headings.append(("suggested-posse", "Suggested Posse"))
        if guide.get("works_well_with") or guide.get("works_well_with_note"):
            headings.append(("works-well-with", "Works Well With"))
        if context.page.meta.get("mythag_teams"):
            headings.append(("example-teams", "Example Teams"))
        if headings:
            placeholder = ET.SubElement(root, "mythag-template-toc")
            for anchor, title in headings:
                ET.SubElement(placeholder, "h2", {"id": anchor}).text = title


class ExtractGuideSections(Postprocessor):
    def run(self, text: str) -> str:
        context = ContextPreprocessor.from_markdown(self.md)
        if context is None or context.page.meta.get("template") != "awakeners/awakener.html":
            return text
        # Markdown also invokes postprocessors while formatting TOC labels.
        # Only capture real section wrappers, not those intermediate fragments.
        sections = SECTION_PATTERN.findall(text)
        if sections:
            context.page.meta["mythag_guide_sections"] = sections
        return TEMPLATE_TOC_PATTERN.sub("", SECTION_PATTERN.sub("", text))


class GuideSectionsExtension(Extension):
    def extendMarkdown(self, md) -> None:
        md.treeprocessors.register(GuideSections(md), "mythag_guide_sections", 6)
        md.postprocessors.register(ExtractGuideSections(md), "mythag_guide_sections", 0)


def makeExtension(**kwargs):
    return GuideSectionsExtension(**kwargs)
