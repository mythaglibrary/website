"""Shared content catalog and validation primitives."""

from __future__ import annotations

import difflib
import re
from collections.abc import Hashable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_IMAGES = ROOT / "lib" / "images"
CONTENT_ROOT = ROOT / "content"
CONTENT_CATEGORIES = ("awakeners", "covenants", "wheels", "posses")
CONTENT_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

type AssetCatalog = dict[str, dict[str, dict[str, str]]]


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silently overwritten mapping keys."""


def _construct_unique_mapping(
    loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, Hashable):
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            )
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_yaml(text: str) -> Any:
    return yaml.load(text, Loader=UniqueKeyLoader)


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    field: str
    message: str
    line: int | None = None
    column: int | None = None

    def __str__(self) -> str:
        location = self.path.as_posix()
        if self.line is not None:
            location += f":{self.line}"
            if self.column is not None:
                location += f":{self.column}"
        if self.field:
            location = f"{location}: {self.field}"
        return f"{location}: {self.message}"


def parse_non_empty_string(value: Any, *, single_line: bool = False) -> tuple[str | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, "expected a non-empty string"
    if value != value.strip():
        return None, "must not have leading or trailing whitespace"
    if single_line and "\n" in value:
        return None, "expected a single-line string"
    return value, None


def parse_content_id(value: Any) -> tuple[str | None, str | None]:
    content_id, error = parse_non_empty_string(value)
    if error is not None:
        return None, error
    assert content_id is not None
    if CONTENT_ID.fullmatch(content_id) is None:
        return None, (
            "expected a lowercase kebab-case content ID such as "
            "burial-grounds-sighs"
        )
    return content_id, None


def unknown_content_id_message(
    category: str, content_id: str, known_ids: dict[str, Any]
) -> str:
    message = f"unknown {category.removesuffix('s')} ID {content_id!r}"
    suggestions = difflib.get_close_matches(content_id, known_ids, n=1, cutoff=0.6)
    if suggestions:
        message += f"; did you mean {suggestions[0]!r}?"
    return message
