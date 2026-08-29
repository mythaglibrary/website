"""Validate Awakener pages and prepare their generated Zensical inputs."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from mythag_site.content import (
    CONTENT_CATEGORIES,
    CONTENT_ID,
    CONTENT_ROOT,
    ROOT,
    SOURCE_IMAGES,
    AssetCatalog,
    ValidationIssue,
    load_yaml,
    parse_content_id,
    parse_non_empty_string,
    unknown_content_id_message,
)
from mythag_site.teams import TeamValidationError


GUIDES_ROOT = ROOT / "lib" / "handbook" / "awakeners"
SOURCE_CONFIG = ROOT / "zensical.toml"
GENERATED_CONFIG = ROOT / ".zensical.generated.toml"
NAV_MARKER = "@mythag-awakener-nav"
TEMPLATE_NAME = "awakeners/awakener.html"

REALM_FAMILIES: tuple[tuple[str, tuple[tuple[str, str | None], ...]], ...] = (
    ("Chaos", (("chaos", None), ("primordia-chaos", "Primordia Chaos"))),
    (
        "Aequor",
        (("aequor", None), ("benthos-aequor", "Benthos Aequor")),
    ),
    ("Caro", (("caro", None), ("propagation-caro", "Propagation Caro"))),
    ("Ultra", (("ultra", None), ("singularity-ultra", "Singularity Ultra"))),
)
KNOWN_REALMS = {
    realm for _, realms in REALM_FAMILIES for realm, _ in realms
}
ALLOWED_AWAKENER_FIELDS = {
    "tagline",
    "roles",
    "ranks",
    "stopping_points",
    "builds",
    "suggested_posses",
    "suggested_posses_note",
    "works_well_with",
    "works_well_with_note",
}
EXTENSION_OWNED_METADATA_FIELDS = {"mythag_teams"}
TIER_STYLE_NAMES = {
    "S": "s",
    "A": "a",
    "B+": "b-plus",
    "B": "b",
    "C+": "c-plus",
    "C": "c",
    "D": "d",
    "F": "f",
}
ALLOWED_TIERS = set(TIER_STYLE_NAMES)
FRONT_MATTER = re.compile(r"\A---[ \t]*\r?\n(?P<yaml>.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
LAYOUT_MARKUP = re.compile(
    r"{{|{%|<!--|<![A-Za-z]|</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*|/?)>"
)


@dataclass(frozen=True)
class Rank:
    tier: str
    note: str | None


@dataclass(frozen=True)
class Recommendation:
    content_id: str
    note: str | None


@dataclass(frozen=True)
class WheelGroups:
    early_game: tuple[Recommendation, ...]
    astral_reign: tuple[Recommendation, ...]


@dataclass(frozen=True)
class Build:
    name: str
    covenants: tuple[str, ...]
    covenants_note: str | None
    wheels: WheelGroups


@dataclass(frozen=True)
class Awakener:
    tagline: str
    roles: tuple[str, ...]
    dps_ranks: tuple[Rank, ...]
    support_ranks: tuple[Rank, ...]
    stopping_points: tuple[str, ...]
    builds: tuple[Build, ...]
    suggested_posses: tuple[Recommendation, ...]
    suggested_posses_note: str | None
    works_well_with: tuple[str, ...]
    works_well_with_note: str | None


@dataclass(frozen=True)
class Guide:
    path: Path
    title: str
    awakener: Awakener

    @property
    def slug(self) -> str:
        return self.path.stem

    @property
    def realm(self) -> str:
        return self.path.parent.name

    @property
    def url(self) -> str:
        source = self.path.relative_to("lib").with_suffix("").as_posix()
        return f"/{source}/"


class AwakenerValidationError(Exception):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        message = "Awakener validation failed:\n" + "\n".join(
            f"- {issue}" for issue in issues
        )
        super().__init__(message)


def _issue(
    issues: list[ValidationIssue], path: Path, field: str, message: str
) -> None:
    issues.append(ValidationIssue(path, field, message))


def _non_empty_string(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
) -> str | None:
    """Accept a non-empty author value exactly as it will be rendered or indexed."""
    parsed, error = parse_non_empty_string(value)
    if error is not None:
        _issue(issues, path, field, error)
        return None
    return parsed


def _content_id(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
) -> str | None:
    content_id, error = parse_content_id(value)
    if error is not None:
        _issue(issues, path, field, error)
        return None
    return content_id


def _report_unknown_fields(
    mapping: dict[Any, Any],
    allowed: set[str],
    issues: list[ValidationIssue],
    path: Path,
    field: str,
    *,
    message: str = "unknown field",
) -> None:
    unknown = (key for key in mapping if key not in allowed)
    for key in sorted(unknown, key=str):
        key_field = f"{field}.{key}" if field else str(key)
        key_message = (
            message if isinstance(key, str) else "expected a string field name"
        )
        _issue(issues, path, key_field, key_message)


def _parsed_string_list(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
    parser: Callable[[Any, list[ValidationIssue], Path, str], str | None],
    *,
    required: bool = True,
) -> list[str]:
    if value is None and not required:
        return []
    if not isinstance(value, list) or (required and not value):
        expectation = "a non-empty list" if required else "a list"
        _issue(issues, path, field, f"expected {expectation}")
        return []

    result: list[str] = []
    for index, item in enumerate(value):
        parsed = parser(item, issues, path, f"{field}[{index}]")
        if parsed is not None:
            result.append(parsed)
    return result


def _string_list(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
    *,
    required: bool = True,
) -> list[str]:
    return _parsed_string_list(
        value, issues, path, field, _non_empty_string, required=required
    )


def _content_id_list(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
    *,
    required: bool = True,
) -> list[str]:
    return _parsed_string_list(
        value, issues, path, field, _content_id, required=required
    )


def _validate_rank_entries(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
) -> list[Rank]:
    if not isinstance(value, list) or not value:
        _issue(issues, path, field, "expected a non-empty list")
        return []
    ranks: list[Rank] = []
    for index, item in enumerate(value):
        item_field = f"{field}[{index}]"
        if not isinstance(item, dict):
            _issue(issues, path, item_field, "expected a mapping")
            continue
        _report_unknown_fields(item, {"tier", "note"}, issues, path, item_field)
        tier = _non_empty_string(item.get("tier"), issues, path, f"{item_field}.tier")
        if tier is not None and tier not in ALLOWED_TIERS:
            _issue(
                issues,
                path,
                f"{item_field}.tier",
                f"expected one of {', '.join(sorted(ALLOWED_TIERS))}",
            )
        note = None
        if "note" in item:
            note = _non_empty_string(item["note"], issues, path, f"{item_field}.note")
        if tier is not None:
            ranks.append(Rank(tier, note))
    return ranks


def _validate_content_recommendations(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
    field: str,
    *,
    required: bool = True,
) -> list[Recommendation]:
    if value is None and not required:
        return []
    if not isinstance(value, list) or (required and not value):
        expectation = "a non-empty list" if required else "a list"
        _issue(issues, path, field, f"expected {expectation}")
        return []

    recommendations: list[Recommendation] = []
    for index, item in enumerate(value):
        item_field = f"{field}[{index}]"
        if not isinstance(item, dict):
            _issue(issues, path, item_field, "expected a mapping with an id")
            continue
        _report_unknown_fields(item, {"id", "note"}, issues, path, item_field)
        content_id = _content_id(item.get("id"), issues, path, f"{item_field}.id")
        note = None
        if "note" in item:
            note = _non_empty_string(item["note"], issues, path, f"{item_field}.note")
        if content_id is not None:
            recommendations.append(Recommendation(content_id, note))
    return recommendations


def _validate_builds(
    value: Any,
    issues: list[ValidationIssue],
    path: Path,
) -> list[Build]:
    if value is None:
        return []
    if not isinstance(value, list):
        _issue(issues, path, "awakener.builds", "expected a list")
        return []

    builds: list[Build] = []
    for index, build in enumerate(value):
        field = f"awakener.builds[{index}]"
        if not isinstance(build, dict):
            _issue(issues, path, field, "expected a mapping")
            continue
        _report_unknown_fields(
            build,
            {"name", "covenants", "covenants_note", "wheels"},
            issues,
            path,
            field,
        )
        name = _non_empty_string(build.get("name"), issues, path, f"{field}.name")
        covenants = _content_id_list(
            build.get("covenants"), issues, path, f"{field}.covenants"
        )
        covenants_note = None
        if "covenants_note" in build:
            covenants_note = _non_empty_string(
                build["covenants_note"], issues, path, f"{field}.covenants_note"
            )

        wheel_groups = build.get("wheels")
        if not isinstance(wheel_groups, dict):
            _issue(issues, path, f"{field}.wheels", "expected a mapping")
            wheel_groups = {}
        _report_unknown_fields(
            wheel_groups,
            {"early_game", "astral_reign"},
            issues,
            path,
            f"{field}.wheels",
        )
        early_game = _validate_content_recommendations(
            wheel_groups.get("early_game"),
            issues,
            path,
            f"{field}.wheels.early_game",
            required=False,
        )
        astral_reign = _validate_content_recommendations(
            wheel_groups.get("astral_reign"),
            issues,
            path,
            f"{field}.wheels.astral_reign",
            required=False,
        )
        if not early_game and not astral_reign:
            _issue(
                issues,
                path,
                f"{field}.wheels",
                "expected at least one non-empty wheel recommendation group",
            )
        if name is not None:
            builds.append(
                Build(
                    name,
                    tuple(covenants),
                    covenants_note,
                    WheelGroups(tuple(early_game), tuple(astral_reign)),
                )
            )
    return builds


def _parse_guide(
    path: Path,
    issues: list[ValidationIssue],
    *,
    validate_location: bool = True,
) -> Guide | None:
    relative = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if match is None:
        _issue(issues, relative, "", "missing leading YAML front matter")
        return None
    try:
        meta = load_yaml(match.group("yaml"))
    except yaml.MarkedYAMLError as error:
        mark = error.problem_mark
        location = "front matter"
        if mark is not None:
            location = f"front matter line {mark.line + 2}, column {mark.column + 1}"
        _issue(issues, relative, location, error.problem or "invalid YAML")
        return None
    if not isinstance(meta, dict):
        _issue(issues, relative, "front matter", "expected a mapping")
        return None
    for field in sorted(EXTENSION_OWNED_METADATA_FIELDS.intersection(meta)):
        _issue(
            issues,
            relative,
            field,
            "reserved extension-owned metadata field",
        )

    body = text[match.end() :]
    if LAYOUT_MARKUP.search(body):
        _issue(
            issues,
            relative,
            "content",
            "use ordinary Markdown; HTML and template expressions are not allowed",
        )

    title = _non_empty_string(meta.get("title"), issues, relative, "title")
    _non_empty_string(meta.get("description"), issues, relative, "description")
    template = _non_empty_string(meta.get("template"), issues, relative, "template")
    if template is not None and template != TEMPLATE_NAME:
        _issue(issues, relative, "template", f"expected {TEMPLATE_NAME!r}")

    awakener = meta.get("awakener")
    if not isinstance(awakener, dict):
        _issue(issues, relative, "awakener", "expected a mapping")
        return None
    _report_unknown_fields(
        awakener, ALLOWED_AWAKENER_FIELDS, issues, relative, "awakener"
    )

    tagline = _non_empty_string(
        awakener.get("tagline"), issues, relative, "awakener.tagline"
    )
    roles = _string_list(awakener.get("roles"), issues, relative, "awakener.roles")

    ranks = awakener.get("ranks")
    dps_ranks: list[Rank] = []
    support_ranks: list[Rank] = []
    if not isinstance(ranks, dict) or not ranks:
        _issue(issues, relative, "awakener.ranks", "expected a non-empty mapping")
    else:
        _report_unknown_fields(
            ranks,
            {"dps", "support"},
            issues,
            relative,
            "awakener.ranks",
            message="unknown rank",
        )
        for key in ("dps", "support"):
            if key in ranks:
                parsed_ranks = _validate_rank_entries(
                    ranks[key], issues, relative, f"awakener.ranks.{key}"
                )
                if key == "dps":
                    dps_ranks = parsed_ranks
                else:
                    support_ranks = parsed_ranks

    stopping_points = _string_list(
        awakener.get("stopping_points"),
        issues,
        relative,
        "awakener.stopping_points",
    )
    builds = _validate_builds(awakener.get("builds"), issues, relative)
    suggested_posses = _validate_content_recommendations(
        awakener.get("suggested_posses"),
        issues,
        relative,
        "awakener.suggested_posses",
        required=False,
    )
    suggested_posses_note = None
    if "suggested_posses_note" in awakener:
        suggested_posses_note = _non_empty_string(
            awakener["suggested_posses_note"],
            issues,
            relative,
            "awakener.suggested_posses_note",
        )
    works_well_with = _content_id_list(
        awakener.get("works_well_with"),
        issues,
        relative,
        "awakener.works_well_with",
        required=False,
    )
    works_well_with_note = None
    if "works_well_with_note" in awakener:
        works_well_with_note = _non_empty_string(
            awakener["works_well_with_note"],
            issues,
            relative,
            "awakener.works_well_with_note",
        )

    if validate_location:
        realm = path.parent.name
        if realm not in KNOWN_REALMS:
            _issue(issues, relative, "", f"unknown realm directory {realm!r}")
    if title is None:
        return None
    slug = path.stem
    if validate_location and CONTENT_ID.fullmatch(slug) is None:
        _issue(
            issues,
            relative,
            "",
            "expected a lowercase kebab-case filename",
        )
    return Guide(
        relative,
        title,
        Awakener(
            tagline or "",
            tuple(roles),
            tuple(dps_ranks),
            tuple(support_ranks),
            tuple(stopping_points),
            tuple(builds),
            tuple(suggested_posses),
            suggested_posses_note,
            tuple(works_well_with),
            works_well_with_note,
        ),
    )


def load_guides() -> tuple[list[Guide], list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    guides = [
        guide
        for path in sorted(GUIDES_ROOT.glob("*/*.md"))
        if (guide := _parse_guide(path, issues)) is not None
    ]

    by_title: dict[str, Guide] = {}
    by_slug: dict[str, Guide] = {}
    for guide in guides:
        for key, index, label in (
            (guide.title.casefold(), by_title, "title"),
            (guide.slug, by_slug, "slug"),
        ):
            if key in index:
                _issue(
                    issues,
                    guide.path,
                    label,
                    f"duplicate {label}; first used by {index[key].path.as_posix()}",
                )
            else:
                index[key] = guide
    return guides, issues


def load_content_catalog(
    issues: list[ValidationIssue],
) -> dict[str, dict[str, str]]:
    catalog = {category: {} for category in CONTENT_CATEGORIES}
    for category in CONTENT_CATEGORIES:
        path = CONTENT_ROOT / f"{category}.yaml"
        relative = path.relative_to(ROOT)
        if not path.is_file():
            _issue(issues, relative, "", "missing content catalog")
            continue
        try:
            entries = load_yaml(path.read_text(encoding="utf-8"))
        except yaml.MarkedYAMLError as error:
            mark = error.problem_mark
            field = ""
            if mark is not None:
                field = f"line {mark.line + 1}, column {mark.column + 1}"
            _issue(issues, relative, field, error.problem or "invalid YAML")
            continue
        if not isinstance(entries, dict):
            _issue(issues, relative, "", "expected a mapping of IDs to labels")
            continue
        for content_id, raw_label in entries.items():
            field = str(content_id)
            parsed_id = _content_id(content_id, issues, relative, field)
            label = _non_empty_string(raw_label, issues, relative, field)
            if parsed_id is not None and label is not None:
                catalog[category][parsed_id] = label
    return catalog


def _catalog_label(
    content_catalog: dict[str, dict[str, str]],
    category: str,
    content_id: str,
    issues: list[ValidationIssue],
    source_path: Path,
    field: str,
) -> str | None:
    label = content_catalog[category].get(content_id)
    if label is not None:
        return label

    message = unknown_content_id_message(category, content_id, content_catalog[category])
    _issue(issues, source_path, field, message)
    return None


def _find_unique_asset(
    pattern: str,
    issues: list[ValidationIssue],
    source_path: Path,
    field: str,
) -> Path | None:
    matches = sorted(SOURCE_IMAGES.glob(pattern))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        _issue(issues, source_path, field, f"no asset matched {pattern!r}")
    else:
        _issue(issues, source_path, field, f"multiple assets matched {pattern!r}")
    return None


def _site_url(path: Path) -> str:
    return "/" + path.relative_to(ROOT / "lib").as_posix()


def _validate_guide_references(
    guides: list[Guide],
    content_catalog: dict[str, dict[str, str]],
    issues: list[ValidationIssue],
    *,
    guide_ids: set[str],
) -> None:
    for guide in guides:
        for content_id in guide.awakener.works_well_with:
            field = "awakener.works_well_with"
            if (
                _catalog_label(
                    content_catalog, "awakeners", content_id, issues, guide.path, field
                )
                is not None
                and content_id not in guide_ids
            ):
                _issue(
                    issues,
                    guide.path,
                    field,
                    f"Awakener ID {content_id!r} does not have a standalone guide",
                )

        for build_index, build in enumerate(guide.awakener.builds):
            for covenant in build.covenants:
                _catalog_label(
                    content_catalog,
                    "covenants",
                    covenant,
                    issues,
                    guide.path,
                    f"awakener.builds[{build_index}].covenants",
                )
            for group, recommendations in (
                ("early_game", build.wheels.early_game),
                ("astral_reign", build.wheels.astral_reign),
            ):
                for item_index, recommendation in enumerate(recommendations):
                    _catalog_label(
                        content_catalog,
                        "wheels",
                        recommendation.content_id,
                        issues,
                        guide.path,
                        f"awakener.builds[{build_index}].wheels.{group}"
                        f"[{item_index}].id",
                    )

        for posse_index, posse in enumerate(guide.awakener.suggested_posses):
            _catalog_label(
                content_catalog,
                "posses",
                posse.content_id,
                issues,
                guide.path,
                f"awakener.suggested_posses[{posse_index}].id",
            )


def validate_guide_catalog(
    guides: list[Guide],
    content_catalog: dict[str, dict[str, str]],
    issues: list[ValidationIssue],
) -> None:
    guide_ids = {guide.slug for guide in guides}
    for guide in guides:
        label = _catalog_label(
            content_catalog, "awakeners", guide.slug, issues, guide.path, "title"
        )
        if label is not None and guide.title != label:
            _issue(issues, guide.path, "title", f"expected catalog label {label!r}")

    catalog_path = (CONTENT_ROOT / "awakeners.yaml").relative_to(ROOT)
    for content_id in sorted(set(content_catalog["awakeners"]) - guide_ids):
        _issue(
            issues,
            catalog_path,
            content_id,
            "does not have a standalone guide",
        )

    _validate_guide_references(
        guides,
        content_catalog,
        issues,
        guide_ids=guide_ids,
    )


def build_asset_catalog(
    guides: list[Guide],
    content_catalog: dict[str, dict[str, str]],
    issues: list[ValidationIssue],
) -> AssetCatalog:
    catalog: AssetCatalog = {
        "portraits": {},
        "awakeners": {},
        "covenants": {},
        "wheels": {},
        "posses": {},
    }
    standalone = {guide.slug: guide for guide in guides}

    awakener_source = (CONTENT_ROOT / "awakeners.yaml").relative_to(ROOT)
    for content_id, label in content_catalog["awakeners"].items():
        target = standalone.get(content_id)
        if target is None:
            continue
        full = _find_unique_asset(
            f"awakeners/*/{content_id}.png", issues, awakener_source, content_id
        )
        mini = _find_unique_asset(
            f"awakeners/*/{content_id}--mini.png", issues, awakener_source, content_id
        )
        if full is None or mini is None:
            continue
        portrait = {"image": _site_url(full), "mini": _site_url(mini)}
        catalog["portraits"][label] = portrait
        catalog["awakeners"][content_id] = {
            "label": label,
            **portrait,
            "url": target.url,
        }

    covenant_source = (CONTENT_ROOT / "covenants.yaml").relative_to(ROOT)
    for content_id, label in content_catalog["covenants"].items():
        full = SOURCE_IMAGES / "covenants" / f"{content_id}.png"
        icon = SOURCE_IMAGES / "covenants" / f"{content_id}--icon.png"
        if not full.is_file():
            _issue(issues, covenant_source, content_id, f"missing {full.relative_to(ROOT)}")
        if not icon.is_file():
            _issue(issues, covenant_source, content_id, f"missing {icon.relative_to(ROOT)}")
        if full.is_file() and icon.is_file():
            catalog["covenants"][content_id] = {
                "label": label,
                "image": _site_url(full),
                "icon": _site_url(icon),
                "url": f"/handbook/team#{content_id}",
            }

    for category in ("wheels", "posses"):
        source = (CONTENT_ROOT / f"{category}.yaml").relative_to(ROOT)
        for content_id, label in content_catalog[category].items():
            image = SOURCE_IMAGES / category / f"{content_id}.png"
            if not image.is_file():
                _issue(issues, source, content_id, f"missing {image.relative_to(ROOT)}")
                continue
            catalog[category][content_id] = {
                "label": label,
                "image": _site_url(image),
            }
    return catalog


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _guides_by_realm(guides: list[Guide]) -> dict[str, list[Guide]]:
    grouped = {realm: [] for realm in KNOWN_REALMS}
    for guide in guides:
        grouped[guide.realm].append(guide)
    for realm_guides in grouped.values():
        realm_guides.sort(key=lambda guide: (guide.title.casefold(), guide.slug))
    return grouped


def _render_nav(guides: list[Guide], indent: str) -> str:
    grouped = _guides_by_realm(guides)

    lines = [f'{indent}{{ "Awakener Guides" = [', f'{indent}  "handbook/awakeners/index.md",']
    for family_name, realms in REALM_FAMILIES:
        if not any(grouped.get(realm) for realm, _ in realms):
            continue
        lines.append(f'{indent}  {{ {_toml_string(family_name)} = [')
        for realm, subgroup_name in realms:
            realm_guides = grouped[realm]
            if not realm_guides:
                continue
            if subgroup_name is not None:
                lines.append(f'{indent}    {{ {_toml_string(subgroup_name)} = [')
            guide_indent = indent + ("      " if subgroup_name is not None else "    ")
            lines.extend(
                f'{guide_indent}{_toml_string(guide.path.relative_to("lib").as_posix())},'
                for guide in realm_guides
            )
            if subgroup_name is not None:
                lines.append(f"{indent}    ]}},")
        lines.append(f"{indent}  ]}},")
    lines.append(f"{indent}]}},")
    return "\n".join(lines)


def _render_catalog(catalog: AssetCatalog) -> str:
    lines = ["", "# Generated by mythag_site.awakeners; do not edit this file."]
    for category in ("portraits", "awakeners", "covenants", "wheels", "posses"):
        lines.append(f"[project.extra.content_assets.{category}]")
        for name, values in sorted(catalog[category].items(), key=lambda item: item[0].casefold()):
            rendered = ", ".join(
                f"{key} = {_toml_string(value)}" for key, value in values.items()
            )
            lines.append(f"{_toml_string(name)} = {{ {rendered} }}")
        lines.append("")
    return "\n".join(lines)


def _toml_string_array(values: list[str]) -> str:
    return "[" + ", ".join(_toml_string(value) for value in values) + "]"


def _render_index(
    guides: list[Guide], catalog: AssetCatalog
) -> str:
    grouped = _guides_by_realm(guides)

    families: list[str] = []
    family_values: list[tuple[str, str, list[str]]] = []
    group_values: list[tuple[str, str | None, list[str]]] = []
    for family_name, realms in REALM_FAMILIES:
        populated_realms = [
            (realm, subgroup_name)
            for realm, subgroup_name in realms
            if grouped[realm]
        ]
        if not populated_realms:
            continue
        family_id = realms[0][0]
        families.append(family_id)
        family_values.append(
            (family_id, family_name, [realm for realm, _ in populated_realms])
        )
        for realm, subgroup_name in populated_realms:
            realm_guides = grouped[realm]
            group_values.append(
                (realm, subgroup_name, [guide.slug for guide in realm_guides])
            )

    lines = [
        "",
        "# Generated by mythag_site.awakeners; do not edit this file.",
        "[project.extra.awakener_index]",
        f"family_order = {_toml_string_array(families)}",
        "[project.extra.awakener_index.family]",
    ]
    for family_id, label, groups in family_values:
        lines.append(
            f"{_toml_string(family_id)} = "
            f"{{ label = {_toml_string(label)}, groups = {_toml_string_array(groups)} }}"
        )

    lines.append("[project.extra.awakener_index.group]")
    for realm, label, guide_ids in group_values:
        rendered_label = _toml_string(label) if label is not None else '""'
        lines.append(
            f"{_toml_string(realm)} = "
            f"{{ label = {rendered_label}, guides = {_toml_string_array(guide_ids)} }}"
        )

    lines.append("[project.extra.awakener_index.guide]")
    for guide in sorted(guides, key=lambda item: item.slug):
        portrait = catalog["portraits"][guide.title]
        values = {
            "label": guide.title,
            "image": portrait["mini"],
            "url": guide.url,
        }
        rendered = ", ".join(
            f"{key} = {_toml_string(value)}" for key, value in values.items()
        )
        lines.append(f"{_toml_string(guide.slug)} = {{ {rendered} }}")
    lines.append("")
    return "\n".join(lines)


def collect_and_validate_awakeners() -> tuple[list[Guide], AssetCatalog]:
    guides, issues = load_guides()
    content_catalog = load_content_catalog(issues)
    validate_guide_catalog(guides, content_catalog, issues)
    catalog = build_asset_catalog(guides, content_catalog, issues)
    if issues:
        raise AwakenerValidationError(issues)
    return guides, catalog


def _content_labels_from_assets(
    catalog: AssetCatalog,
) -> dict[str, dict[str, str]]:
    return {
        category: {
            content_id: values["label"]
            for content_id, values in catalog[category].items()
        }
        for category in CONTENT_CATEGORIES
    }


def validate_reference_examples(
    catalog: AssetCatalog,
    guide_ids: set[str],
) -> list[ValidationIssue]:
    """Validate repository-only examples without publishing them as guides."""
    examples_root = ROOT / "examples"
    if not examples_root.is_dir():
        return []

    issues: list[ValidationIssue] = []
    guide_path = examples_root / "awakener-guide.md"
    if not guide_path.is_file():
        _issue(issues, guide_path.relative_to(ROOT), "", "missing reference example")
    else:
        example = _parse_guide(guide_path, issues, validate_location=False)
        if example is not None:
            _validate_guide_references(
                [example],
                _content_labels_from_assets(catalog),
                issues,
                guide_ids=guide_ids,
            )

    team_path = examples_root / "team-fence.md"
    if not team_path.is_file():
        _issue(issues, team_path.relative_to(ROOT), "", "missing reference example")
    return issues


def render_generated_config(guides: list[Guide], catalog: AssetCatalog) -> str:
    source = SOURCE_CONFIG.read_text(encoding="utf-8")
    marker = re.compile(
        rf"^(?P<indent>[ \t]*).*{re.escape(NAV_MARKER)}.*$", re.MULTILINE
    )
    match = marker.search(source)
    if match is None:
        raise AwakenerValidationError(
            [ValidationIssue(SOURCE_CONFIG.relative_to(ROOT), "", f"missing {NAV_MARKER}")]
        )
    generated = marker.sub(
        _render_nav(guides, match.group("indent")), source, count=1
    ).rstrip()
    generated += "\n" + _render_index(guides, catalog)
    generated += "\n" + _render_catalog(catalog)
    try:
        tomllib.loads(generated)
    except tomllib.TOMLDecodeError as error:
        raise AwakenerValidationError(
            [
                ValidationIssue(
                    SOURCE_CONFIG.relative_to(ROOT),
                    "",
                    f"generated config is invalid TOML: {error}",
                )
            ]
        ) from error
    return generated


def write_generated_config(generated: str) -> None:
    temporary = GENERATED_CONFIG.with_suffix(".tmp.toml")
    temporary.write_text(generated, encoding="utf-8", newline="\n")
    temporary.replace(GENERATED_CONFIG)


def prepare_awakeners() -> list[Guide]:
    guides, catalog = collect_and_validate_awakeners()
    write_generated_config(render_generated_config(guides, catalog))
    return guides


def check_main() -> None:
    try:
        guides, catalog = collect_and_validate_awakeners()
        render_generated_config(guides, catalog)
        from mythag_site.team_extension import validate_team_document  # noqa: PLC0415
        markdown_roots = (ROOT / "lib", ROOT / "examples")
        team_issues = [
            issue
            for root in markdown_roots
            for path in sorted(root.rglob("*.md"))
            for issue in validate_team_document(path, catalog)
        ]
        reference_issues = validate_reference_examples(
            catalog,
            {guide.slug for guide in guides},
        )
        if team_issues or reference_issues:
            raise TeamValidationError([*team_issues, *reference_issues])
    except AwakenerValidationError as error:
        raise SystemExit(str(error)) from error
    except TeamValidationError as error:
        raise SystemExit(str(error)) from error
    print(f"Content: {len(guides)} Awakener guides and inline teams valid")


def serve_main() -> None:
    try:
        guides = prepare_awakeners()
    except AwakenerValidationError as error:
        raise SystemExit(str(error)) from error
    print(
        f"Awakener content: {len(guides)} guides valid; "
        "fast preview only (run mythag-build for production output); "
        "restart after adding, renaming, or removing a guide"
    )
    subprocess.run(
        [sys.executable, "-m", "zensical", "serve", "--config-file", str(GENERATED_CONFIG)],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    check_main()
