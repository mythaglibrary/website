"""Render validated inline team builds in Markdown pages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from yaml.nodes import MappingNode, Node, SequenceNode

from mythag_site.content import (
    ROOT,
    AssetCatalog,
    UniqueKeyLoader,
    ValidationIssue,
    parse_content_id,
    parse_non_empty_string,
    unknown_content_id_message,
)


TEMPLATE_ROOT = ROOT / "overrides"
TEMPLATE_NAME = "teams/team.html"
TEAM_ARCHETYPES = frozenset({"dps", "support", "tank"})
TEAM_ARCHETYPE_LABELS = {"dps": "DPS", "support": "Support", "tank": "Tank"}


@dataclass(frozen=True)
class TeamMemberSpec:
    awakener_id: str
    covenant_id: str
    wheel_ids: tuple[str, str]
    role: str | None
    archetype: str | None
    note: str | None


@dataclass(frozen=True)
class TeamSpec:
    name: str
    posse_id: str
    members: tuple[TeamMemberSpec, ...]
    context: str | None
    summary: str | None


@dataclass(frozen=True)
class TeamAsset:
    label: str
    image: str


@dataclass(frozen=True)
class LinkedTeamAsset:
    label: str
    image: str
    url: str


@dataclass(frozen=True)
class TeamMemberView:
    awakener: LinkedTeamAsset
    covenant: LinkedTeamAsset
    wheels: tuple[TeamAsset, TeamAsset]
    role: str | None
    archetype: str | None
    archetype_label: str | None
    note: str | None


@dataclass(frozen=True)
class TeamView:
    name: str
    posse: TeamAsset
    members: tuple[TeamMemberView, ...]
    context: str | None
    summary: str | None


@dataclass(frozen=True)
class TeamFence:
    source: str
    opening_line: int


class TeamValidationError(Exception):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        super().__init__(
            "Team validation failed:\n" + "\n".join(f"- {issue}" for issue in issues)
        )


def _collect_marks(node: Node, path: str, marks: dict[str, yaml.Mark]) -> None:
    marks[path] = node.start_mark
    if isinstance(node, MappingNode):
        for key_node, value_node in node.value:
            key = key_node.value
            child = f"{path}.{key}" if path else key
            marks[f"{child}#key"] = key_node.start_mark
            _collect_marks(value_node, child, marks)
    elif isinstance(node, SequenceNode):
        for index, value_node in enumerate(node.value):
            _collect_marks(value_node, f"{path}[{index}]", marks)


def _parse_yaml(source: str) -> tuple[Any, dict[str, yaml.Mark]]:
    loader = UniqueKeyLoader(source)
    try:
        node = loader.get_single_node()
        if node is None:
            return None, {}
        marks: dict[str, yaml.Mark] = {}
        _collect_marks(node, "", marks)
        return loader.construct_document(node), marks
    finally:
        loader.dispose()


class _TeamValidator:
    """Validation state for one authored team fence."""

    def __init__(
        self, path: Path, fence: TeamFence, marks: dict[str, yaml.Mark]
    ) -> None:
        self.path = path
        self.fence = fence
        self.marks = marks
        self.issues: list[ValidationIssue] = []

    def mark_for(self, field: str) -> yaml.Mark | None:
        if field in self.marks:
            return self.marks[field]
        if "." in field:
            return self.marks.get(field.rsplit(".", 1)[0])
        return self.marks.get("")

    def issue(
        self,
        field: str,
        message: str,
        *,
        mark: yaml.Mark | None = None,
    ) -> None:
        source_mark = mark or self.mark_for(field)
        yaml_line = source_mark.line if source_mark is not None else 0
        yaml_column = source_mark.column if source_mark is not None else 0
        self.issues.append(
            ValidationIssue(
                self.path,
                field,
                message,
                line=self.fence.opening_line + 1 + yaml_line,
                column=yaml_column + 1,
            )
        )

    def mapping(self, value: Any, field: str) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            self.issue(field, "expected a mapping")
            return None
        return value

    def string(self, value: Any, field: str) -> str | None:
        parsed, error = parse_non_empty_string(value, single_line=True)
        if error is not None:
            self.issue(field, error)
            return None
        return parsed

    def content_id(
        self,
        value: Any,
        assets: dict[str, dict[str, str]],
        category: str,
        field: str,
    ) -> str | None:
        content_id, error = parse_content_id(value)
        if error is not None:
            self.issue(field, error)
            return None
        assert content_id is not None
        if content_id not in assets:
            self.issue(
                field, unknown_content_id_message(category, content_id, assets)
            )
            return None
        return content_id

    def fields(
        self,
        value: dict[str, Any],
        allowed: set[str],
        field: str = "",
        *,
        required: set[str] | None = None,
    ) -> None:
        for key in value:
            child = f"{field}.{key}" if field else str(key)
            if key not in allowed:
                self.issue(
                    child,
                    "unknown field",
                    mark=self.marks.get(f"{child}#key"),
                )
        for key in (required if required is not None else allowed) - value.keys():
            child = f"{field}.{key}" if field else key
            self.issue(child, "missing required field", mark=self.mark_for(field))


def parse_team(fence: TeamFence, path: Path, assets: AssetCatalog) -> TeamSpec:
    try:
        raw, marks = _parse_yaml(fence.source)
    except yaml.MarkedYAMLError as error:
        validator = _TeamValidator(path, fence, {})
        validator.issue(
            "team", error.problem or "invalid YAML", mark=error.problem_mark
        )
        raise TeamValidationError(validator.issues) from error

    validator = _TeamValidator(path, fence, marks)
    root = validator.mapping(raw, "team")
    if root is None:
        raise TeamValidationError(validator.issues)
    validator.fields(
        root,
        {"name", "context", "summary", "posse", "members"},
        required={"name", "posse", "members"},
    )
    name = validator.string(root.get("name"), "name")
    context = (
        validator.string(root["context"], "context")
        if "context" in root
        else None
    )
    summary = (
        validator.string(root["summary"], "summary")
        if "summary" in root
        else None
    )
    posse_id = validator.content_id(
        root.get("posse"),
        assets["posses"],
        "posses",
        "posse",
    )

    members_raw = root.get("members")
    if not isinstance(members_raw, list):
        validator.issue(
            "members",
            "expected a list of exactly four members",
        )
        members_raw = []
    elif len(members_raw) != 4:
        validator.issue("members", "expected exactly four members")

    members: list[TeamMemberSpec] = []
    for index, member_raw in enumerate(members_raw):
        prefix = f"members[{index}]"
        member = validator.mapping(member_raw, prefix)
        if member is None:
            continue
        validator.fields(
            member,
            {"awakener", "covenant", "wheels", "role", "archetype", "note"},
            prefix,
            required={"awakener", "covenant", "wheels", "archetype"},
        )
        role = (
            validator.string(member["role"], f"{prefix}.role")
            if "role" in member
            else None
        )
        archetype = (
            validator.string(member["archetype"], f"{prefix}.archetype")
            if "archetype" in member
            else None
        )
        if archetype is not None and archetype not in TEAM_ARCHETYPES:
            validator.issue(
                f"{prefix}.archetype",
                "expected one of: dps, support, tank",
            )
        note = (
            validator.string(member["note"], f"{prefix}.note")
            if "note" in member
            else None
        )
        awakener_id = validator.content_id(
            member.get("awakener"),
            assets["awakeners"],
            "awakeners",
            f"{prefix}.awakener",
        )
        covenant_id = validator.content_id(
            member.get("covenant"),
            assets["covenants"],
            "covenants",
            f"{prefix}.covenant",
        )
        wheels_raw = member.get("wheels")
        wheel_ids: list[str] = []
        if not isinstance(wheels_raw, list) or len(wheels_raw) != 2:
            validator.issue(
                f"{prefix}.wheels",
                "expected exactly two wheel IDs",
            )
        else:
            for wheel_index, wheel_raw in enumerate(wheels_raw):
                wheel_id = validator.content_id(
                    wheel_raw,
                    assets["wheels"],
                    "wheels",
                    f"{prefix}.wheels[{wheel_index}]",
                )
                if wheel_id is not None:
                    wheel_ids.append(wheel_id)
        if awakener_id and covenant_id and len(wheel_ids) == 2:
            members.append(
                TeamMemberSpec(
                    awakener_id,
                    covenant_id,
                    (wheel_ids[0], wheel_ids[1]),
                    role,
                    archetype,
                    note,
                )
            )

    if validator.issues or name is None or posse_id is None or len(members) != 4:
        raise TeamValidationError(validator.issues)
    return TeamSpec(name, posse_id, tuple(members), context, summary)


def _asset(
    assets: AssetCatalog,
    category: str,
    content_id: str,
) -> TeamAsset:
    item = assets[category][content_id]
    return TeamAsset(item["label"], item["image"])


def _linked_asset(
    assets: AssetCatalog,
    category: str,
    content_id: str,
) -> LinkedTeamAsset:
    item = assets[category][content_id]
    image = item["icon"] if category == "covenants" else item["image"]
    return LinkedTeamAsset(item["label"], image, item["url"])


def resolve_team(spec: TeamSpec, assets: AssetCatalog) -> TeamView:
    members = tuple(
        TeamMemberView(
            awakener=_linked_asset(assets, "awakeners", member.awakener_id),
            covenant=_linked_asset(assets, "covenants", member.covenant_id),
            wheels=(
                _asset(assets, "wheels", member.wheel_ids[0]),
                _asset(assets, "wheels", member.wheel_ids[1]),
            ),
            role=member.role,
            archetype=member.archetype,
            archetype_label=TEAM_ARCHETYPE_LABELS.get(member.archetype),
            note=member.note,
        )
        for member in spec.members
    )
    return TeamView(
        spec.name,
        _asset(assets, "posses", spec.posse_id),
        members,
        spec.context,
        spec.summary,
    )


_TEMPLATES = Environment(
    loader=FileSystemLoader(TEMPLATE_ROOT),
    autoescape=select_autoescape(("html",)),
    undefined=StrictUndefined,
    auto_reload=True,
)


def render_team(team: TeamView) -> str:
    return _TEMPLATES.get_template(TEMPLATE_NAME).render(team=team)
