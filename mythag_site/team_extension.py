"""Zensical transport for inline team fences."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from zensical.extensions.context import ContextPreprocessor

from mythag_site.content import ROOT, AssetCatalog, ValidationIssue
from mythag_site.teams import (
    TeamFence,
    TeamValidationError,
    parse_team,
    render_team,
    resolve_team,
)


FENCE_INDENT = r" {0,3}"
TEAM_OPEN = re.compile(r"^(?P<fence>`{3,})team[ \t]*$")
TEAM_INDENTED = re.compile(r"^[ \t]+`{3,}team[ \t]*$")
TEAM_CONTAINER = re.compile(
    r"^ {0,3}(?:(?:>[ \t]*)+(?:(?:[-+*]|\d+[.)])[ \t]+)*|"
    r"(?:(?:[-+*]|\d+[.)])[ \t]+)+)`{3,}team[ \t]*$"
)
TEAM_TABLE = re.compile(r"^\s*\|(?:[^|]*\|)*\s*`{3,}team[ \t]*(?:\|.*)?$")
AWAKENER_TEMPLATE_NAME = "awakeners/awakener.html"
FENCE_OPEN = re.compile(
    rf"^{FENCE_INDENT}(?P<fence>`{{3,}}|~{{3,}})(?:[^`~].*)?$"
)
FRONT_MATTER = re.compile(
    r"^-{3}[ \r\t]*?\n(.*?\r?\n)(?:\.{3}|-{3})[ \r\t]*\n",
    re.UNICODE | re.DOTALL,
)


def _closing_fence(line: str, fence: str) -> bool:
    return (
        re.fullmatch(
            rf"^{FENCE_INDENT}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$", line
        )
        is not None
    )


def _team_open(line: str) -> re.Match[str] | None:
    return TEAM_OPEN.fullmatch(line)


def _team_indented(line: str) -> bool:
    return TEAM_INDENTED.fullmatch(line) is not None


def _team_container(line: str) -> bool:
    return (
        TEAM_CONTAINER.fullmatch(line) is not None
        or TEAM_TABLE.fullmatch(line) is not None
    )


def scan_team_fences(
    lines: list[str], path: Path, *, line_offset: int = 0
) -> list[str | TeamFence]:
    output: list[str | TeamFence] = []
    outer_fence: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if outer_fence is not None:
            output.append(line)
            if _closing_fence(line, outer_fence):
                outer_fence = None
            index += 1
            continue
        team_open = _team_open(line)
        if team_open is not None:
            team_fence = team_open.group("fence")
            closing = index + 1
            while closing < len(lines) and not _closing_fence(
                lines[closing], team_fence
            ):
                closing += 1
            if closing == len(lines):
                raise TeamValidationError(
                    [
                        ValidationIssue(
                            path,
                            "team",
                            "missing closing team fence",
                            index + 1 + line_offset,
                            1,
                        )
                    ]
                )
            output.append(
                TeamFence(
                    "\n".join(lines[index + 1 : closing]),
                    index + 1 + line_offset,
                )
            )
            output.extend("" for _ in range(closing - index))
            index = closing + 1
            continue
        if _team_indented(line) or _team_container(line):
            raise TeamValidationError(
                [
                    ValidationIssue(
                        path,
                        "team",
                        "team blocks must be standalone top-level Markdown; "
                        "nested tables, lists, blockquotes, admonitions, and tabs "
                        "are not supported",
                        index + 1 + line_offset,
                        1,
                    )
                ]
            )
        match = FENCE_OPEN.fullmatch(line)
        if match is not None:
            outer_fence = match.group("fence")
        output.append(line)
        index += 1
    return output


def _needs_team_processing(lines: list[str]) -> bool:
    try:
        segments = scan_team_fences(lines, Path("<markdown>"))
    except TeamValidationError:
        return True
    return any(isinstance(segment, TeamFence) for segment in segments)


def _strip_front_matter(source: str) -> tuple[str, int]:
    body = source
    start_line = 1
    if match := FRONT_MATTER.match(source):
        body = source[match.end() :]
        start_line = source[: match.end()].count("\n") + 1
        stripped = len(body) - len(body.lstrip("\n"))
        body = body.lstrip("\n")
        start_line += stripped
    return body, start_line


def validate_team_document(path: Path, assets: AssetCatalog) -> list[ValidationIssue]:
    relative = path.relative_to(ROOT)
    try:
        source = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        body, start_line = _strip_front_matter(source)
        for segment in scan_team_fences(
            body.split("\n"), relative, line_offset=start_line - 1
        ):
            if isinstance(segment, TeamFence):
                parse_team(segment, relative, assets)
    except TeamValidationError as error:
        return error.issues
    return []


def _context_or_error(md: Markdown) -> Any:
    context = ContextPreprocessor.from_markdown(md)
    if context is None:
        raise TeamValidationError(
            [ValidationIssue(Path("<markdown>"), "team", "missing Zensical page context")]
        )
    return context


def _source_context(md: Markdown, lines: list[str]) -> tuple[Path, int]:
    context = _context_or_error(md)
    page_path = Path(context.page.path)
    candidates = (
        [page_path]
        if page_path.is_absolute()
        else [ROOT / page_path, ROOT / "lib" / page_path]
    )
    source_path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if source_path is None:
        raise TeamValidationError(
            [ValidationIssue(page_path, "team", "could not locate source page")]
        )
    source = source_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    body, start_line = _strip_front_matter(source)
    normalized = (body + "\n\n").expandtabs(md.tab_length)
    normalized = re.sub(r"(?<=\n) +\n", "\n", normalized)
    expected_lines = normalized.split("\n")
    if lines[: len(expected_lines)] != expected_lines:
        relative = source_path.relative_to(ROOT)
        mismatch = next(
            (
                index
                for index, (expected, actual) in enumerate(zip(expected_lines, lines))
                if expected != actual
            ),
            min(len(expected_lines), len(lines)),
        )
        raise TeamValidationError(
            [
                ValidationIssue(
                    relative,
                    "team",
                    "could not align rendered Markdown with its source "
                    f"(first mismatch at body line {mismatch + 1}; "
                    f"expected at least {len(expected_lines)} lines, received {len(lines)})",
                )
            ]
        )
    return source_path.relative_to(ROOT), start_line


class TeamPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        if not _needs_team_processing(lines):
            return lines
        context = _context_or_error(self.md)
        path, start_line = _source_context(self.md, lines)
        assets = context.config["extra"]["content_assets"]
        is_awakener_guide = (
            context.page.meta.get("template") == AWAKENER_TEMPLATE_NAME
        )
        awakener_teams: list[str] = []
        output: list[str] = []
        for segment in scan_team_fences(lines, path, line_offset=start_line - 1):
            if isinstance(segment, str):
                output.append(segment)
                continue
            team = resolve_team(parse_team(segment, path, assets), assets)
            rendered = render_team(team).replace("\n", "")
            if is_awakener_guide:
                awakener_teams.append(rendered)
                output.append("")
            else:
                output.append(rendered)
        if is_awakener_guide:
            context.page.meta["mythag_teams"] = awakener_teams
        return output


class TeamExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(TeamPreprocessor(md), "mythag_team", 29)


def makeExtension(**kwargs: Any) -> TeamExtension:
    return TeamExtension(**kwargs)
