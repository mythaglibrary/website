from __future__ import annotations

import unittest
from contextlib import ExitStack, contextmanager
from tempfile import TemporaryDirectory
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from mythag_site import awakeners, team_extension
from mythag_site.team_extension import scan_team_fences
from mythag_site.teams import (
    TeamFence,
    TeamValidationError,
    parse_team,
    render_team,
    resolve_team,
)


def asset(label: str, image: str, url: str | None = None) -> dict[str, str]:
    value = {"label": label, "image": image}
    if url is not None:
        value["url"] = url
    return value


ASSETS = {
    "portraits": {},
    "awakeners": {
        "member-a": asset(
            "Awakener A", "/images/member-a.png", "/awakeners/member-a/"
        ),
        "member-b": asset(
            "Awakener B", "/images/member-b.png", "/awakeners/member-b/"
        ),
        "member-c": asset(
            "Awakener C", "/images/member-c.png", "/awakeners/member-c/"
        ),
        "member-d": asset(
            "Awakener D", "/images/member-d.png", "/awakeners/member-d/"
        ),
    },
    "covenants": {
        covenant: {
            **asset(
                covenant.replace("-", " ").title(),
                f"/images/{covenant}.png",
                f"/team#{covenant}",
            ),
            "icon": f"/images/{covenant}--icon.png",
        }
        for covenant in (
            "covenant-a",
            "covenant-b",
            "covenant-c",
            "covenant-d",
        )
    },
    "wheels": {
        wheel: asset(wheel.replace("-", " ").title(), f"/images/{wheel}.png")
        for wheel in (
            "wheel-a",
            "wheel-b",
            "wheel-c",
            "wheel-d",
            "wheel-e",
            "wheel-f",
            "wheel-g",
            "wheel-h",
        )
    },
    "posses": {
        "posse-a": asset("Posse A", "/images/posse-a.png")
    },
}

VALID_TEAM = """\
name: Example Team
posse: posse-a
members:
  - awakener: member-a
    archetype: dps
    covenant: covenant-a
    wheels: [wheel-a, wheel-b]
  - awakener: member-b
    archetype: support
    covenant: covenant-b
    wheels: [wheel-c, wheel-d]
  - awakener: member-c
    archetype: support
    covenant: covenant-c
    wheels: [wheel-e, wheel-f]
  - awakener: member-d
    archetype: tank
    covenant: covenant-d
    wheels: [wheel-g, wheel-h]
"""

RENDERABLE_TEAM = VALID_TEAM
for member_id in ("member-a", "member-b", "member-c", "member-d"):
    RENDERABLE_TEAM = RENDERABLE_TEAM.replace(member_id, "example")

TEMP_CATALOGS = {
    category: {
        content_id: values["label"]
        for content_id, values in ASSETS[category].items()
    }
    for category in ("covenants", "wheels", "posses")
}


class TeamTests(unittest.TestCase):
    AWAKENER_GUIDE = """\
---
title: Example
description: Example guide.
template: awakeners/awakener.html
awakener:
  tagline: Example tagline
  roles: [Support]
  ranks:
    support:
      - tier: B
        note: Decent
  stopping_points: [E0]
  builds: []
  suggested_posses: []
  works_well_with: []
---

"""

    def temp_project(self, root: Path, document: str) -> None:
        guide = root / "lib" / "handbook" / "awakeners" / "chaos" / "example.md"
        guide.parent.mkdir(parents=True, exist_ok=True)
        guide.write_text(document, encoding="utf-8")

        images = root / "lib" / "images"
        portraits = images / "awakeners" / "chaos"
        portraits.mkdir(parents=True)
        (portraits / "example.png").write_bytes(b"png")
        (portraits / "example--mini.png").write_bytes(b"png")
        content_root = root / "content"
        content_root.mkdir()
        for category, entries in TEMP_CATALOGS.items():
            (content_root / f"{category}.yaml").write_text(
                "\n".join(
                    f"{content_id}: {label}"
                    for content_id, label in entries.items()
                )
                + "\n",
                encoding="utf-8",
            )
            category_root = images / category
            category_root.mkdir(parents=True)
            for content_id in entries:
                (category_root / f"{content_id}.png").write_bytes(b"png")
                if category == "covenants":
                    (category_root / f"{content_id}--icon.png").write_bytes(b"png")

        (content_root / "awakeners.yaml").write_text(
            "example: Example\n", encoding="utf-8"
        )
        (root / "zensical.toml").write_text(
            "[project]\n"
            'docs_dir = "lib"\n'
            'site_name = "Test"\n'
            'nav = [\n'
            '  { "Awakener Guides" = "handbook/awakeners.md" }, '
            '# @mythag-awakener-nav\n'
            ']\n'
            '\n[project.markdown_extensions."mythag_site.team_extension"]\n',
            encoding="utf-8",
        )

    @contextmanager
    def prepared_temp_project(self, root: Path, document: str):
        self.temp_project(root, document)
        with ExitStack() as stack:
            stack.enter_context(patch.object(awakeners, "ROOT", root))
            stack.enter_context(
                patch.object(
                    awakeners, "GUIDES_ROOT", root / "lib" / "handbook" / "awakeners"
                )
            )
            stack.enter_context(
                patch.object(awakeners, "CONTENT_ROOT", root / "content")
            )
            stack.enter_context(
                patch.object(awakeners, "SOURCE_IMAGES", root / "lib" / "images")
            )
            stack.enter_context(
                patch.object(awakeners, "SOURCE_CONFIG", root / "zensical.toml")
            )
            stack.enter_context(
                patch.object(
                    awakeners,
                    "GENERATED_CONFIG",
                    root / ".zensical.generated.toml",
                )
            )
            stack.enter_context(patch.object(team_extension, "ROOT", root))
            yield

    def test_valid_team_resolves_catalog_data_and_escapes_author_text(self) -> None:
        spec = parse_team(
            TeamFence(VALID_TEAM.replace("Example Team", "Example & Friends"), 10),
            Path("guide.md"),
            ASSETS,
        )
        view = resolve_team(spec, ASSETS)
        rendered = render_team(view)

        self.assertIn("Example &amp; Friends", rendered)
        self.assertIn('/awakeners/member-a/', rendered)
        self.assertIn('/images/covenant-a--icon.png', rendered)
        self.assertIn('title="Awakener A"', rendered)
        self.assertIn('title="Covenant A"', rendered)
        self.assertIn('title="Wheel A"', rendered)
        self.assertEqual(rendered.count('title="Wheel A"'), 1)
        self.assertEqual(rendered.count('<li class="mythag-team__member'), 4)
        self.assertEqual(view.members[0].archetype_label, "DPS")
        self.assertIn('class="mythag-team__role">DPS</p>', rendered)
        self.assertIn('class="mythag-team__role">Support</p>', rendered)
        self.assertIn('class="mythag-team__role">Tank</p>', rendered)
        self.assertNotIn(">Dps<", rendered)

    def test_accepts_optional_team_narrative_fields(self) -> None:
        source = (
            VALID_TEAM.replace(
                "posse: posse-a",
                "context: Example mode\nsummary: An example team\nposse: posse-a",
            )
            .replace(
                "    archetype: dps\n",
                "    archetype: dps\n    role: Example role\n    note: Example note\n",
            )
        )

        spec = parse_team(TeamFence(source, 10), Path("guide.md"), ASSETS)
        rendered = render_team(resolve_team(spec, ASSETS))

        self.assertEqual(spec.summary, "An example team")
        self.assertEqual(spec.context, "Example mode")
        self.assertEqual(spec.members[0].archetype, "dps")
        self.assertEqual(spec.members[0].role, "Example role")
        self.assertEqual(spec.members[0].note, "Example note")
        self.assertIn("An example team", rendered)
        self.assertIn('class="mythag-team__eyebrow">Example mode</p>', rendered)
        self.assertIn('data-archetype="dps"', rendered)
        self.assertIn("Example role", rendered)
        self.assertIn("Example note", rendered)

    def test_rejects_unknown_team_archetype(self) -> None:
        source = VALID_TEAM.replace(
            "    archetype: dps\n",
            "    archetype: striker\n",
        )

        with self.assertRaises(TeamValidationError) as caught:
            parse_team(TeamFence(source, 10), Path("guide.md"), ASSETS)

        issue = caught.exception.issues[0]
        self.assertEqual(issue.field, "members[0].archetype")
        self.assertEqual(issue.message, "expected one of: dps, support, tank")

    def test_rejects_missing_team_archetype(self) -> None:
        source = VALID_TEAM.replace("    archetype: dps\n", "", 1)

        with self.assertRaises(TeamValidationError) as caught:
            parse_team(TeamFence(source, 10), Path("guide.md"), ASSETS)

        issue = caught.exception.issues[0]
        self.assertEqual(issue.field, "members[0].archetype")
        self.assertEqual(issue.message, "missing required field")

    def test_rejects_invalid_team_shape(self) -> None:
        cases = (
            (
                "member count",
                VALID_TEAM[: VALID_TEAM.index("members:")] + "members: []\n",
                "members",
                "expected exactly four members",
            ),
            (
                "wheel count",
                VALID_TEAM.replace(
                    "wheels: [wheel-a, wheel-b]", "wheels: [wheel-a]", 1
                ),
                "members[0].wheels",
                "expected exactly two wheel IDs",
            ),
        )

        for name, source, field, message in cases:
            with self.subTest(name=name):
                with self.assertRaises(TeamValidationError) as caught:
                    parse_team(TeamFence(source, 10), Path("guide.md"), ASSETS)

                issues = caught.exception.issues
                self.assertTrue(any(issue.field == field for issue in issues))
                self.assertTrue(any(issue.message == message for issue in issues))

    def test_unknown_id_reports_physical_location_and_suggestion(self) -> None:
        source = VALID_TEAM.replace("wheel-b", "wheel-bx")
        with self.assertRaises(TeamValidationError) as caught:
            parse_team(TeamFence(source, 10), Path("guide.md"), ASSETS)

        issue = caught.exception.issues[0]
        self.assertEqual(issue.field, "members[0].wheels[1]")
        self.assertIn("unknown wheel ID 'wheel-bx'", issue.message)
        self.assertIn("did you mean 'wheel-b'", issue.message)
        self.assertIsNotNone(issue.line)
        self.assertIsNotNone(issue.column)

    def test_scanner_ignores_examples_and_rejects_unclosed_teams(self) -> None:
        example = ["  ````markdown", "  ```team", VALID_TEAM, "  ```", "  ````"]
        self.assertFalse(
            any(
                isinstance(segment, TeamFence)
                for segment in scan_team_fences(example, Path("guide.md"))
            )
        )
        self.assertEqual(team_extension.TeamPreprocessor(None).run(example), example)

        with self.assertRaises(TeamValidationError) as caught:
            scan_team_fences(
                ["before", "```team", VALID_TEAM],
                Path("guide.md"),
                line_offset=4,
            )
        issue = caught.exception.issues[0]
        self.assertEqual(issue.field, "team")
        self.assertEqual(issue.message, "missing closing team fence")
        self.assertEqual(issue.line, 6)

    def test_scanner_accepts_team_fence_trailing_whitespace(self) -> None:
        segments = scan_team_fences(
            ["```team   ", *VALID_TEAM.splitlines(), "   ```   "],
            Path("guide.md"),
        )

        team_segments = [
            segment for segment in segments if isinstance(segment, TeamFence)
        ]
        self.assertEqual(len(team_segments), 1)
        self.assertIn("name: Example Team", team_segments[0].source)

    def test_scanner_accepts_long_team_fences_and_requires_matching_close(self) -> None:
        segments = scan_team_fences(
            ["````team", *VALID_TEAM.splitlines(), "   `````"],
            Path("guide.md"),
        )

        team_segments = [
            segment for segment in segments if isinstance(segment, TeamFence)
        ]
        self.assertEqual(len(team_segments), 1)

        with self.assertRaises(TeamValidationError) as caught:
            scan_team_fences(
                ["````team", *VALID_TEAM.splitlines(), "```"],
                Path("guide.md"),
            )
        self.assertEqual(caught.exception.issues[0].line, 1)

    def test_scanner_rejects_nested_team_fence(self) -> None:
        for opener in (
            "  ```team",
            "    ```team",
            "\t```team",
            "- ```team",
            "- ````team",
            "> ```team",
            "> > ```team",
            "> - ```team",
            "- - ```team",
            "| ```team |",
        ):
            with self.subTest(opener=repr(opener)):
                with self.assertRaises(TeamValidationError) as caught:
                    scan_team_fences(
                        [opener, *VALID_TEAM.splitlines(), "    ```"],
                        Path("guide.md"),
                    )

                issue = caught.exception.issues[0]
                self.assertEqual(issue.field, "team")
                self.assertTrue(
                    issue.message.startswith(
                        "team blocks must be standalone top-level Markdown"
                    )
                )

    def test_validator_ignores_team_like_front_matter(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "guide.md"
            source.write_text(
                "---\n"
                "description: |\n"
                "  ```team\n"
                "---\n"
                "Body.\n",
                encoding="utf-8",
            )

            with patch.object(team_extension, "ROOT", root):
                self.assertEqual(
                    team_extension.validate_team_document(source, ASSETS), []
                )

    def test_zensical_renders_frontmatter_page_at_the_authored_position(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lib" / "handbook" / "example.md"
            source.parent.mkdir(parents=True)
            document = (
                "---\ntitle: Example team\n---\n\n"
                f"Before.\n\n```team   \n{RENDERABLE_TEAM}```   \n\nAfter.\n"
            )
            source.write_text(document, encoding="utf-8")

            import zensical.config as zensical_config
            from zensical.markdown.render import render

            previous_config = zensical_config._CONFIG
            try:
                with self.prepared_temp_project(root, self.AWAKENER_GUIDE):
                    awakeners.prepare_awakeners()
                    zensical_config.parse_zensical_config(
                        str(awakeners.GENERATED_CONFIG)
                    )
                    rendered = render(
                        document,
                        "handbook/example.md",
                        "/handbook/example/",
                    )["content"]
            finally:
                zensical_config._CONFIG = previous_config

        self.assertLess(rendered.index("Before."), rendered.index("mythag-team"))
        self.assertLess(rendered.index("mythag-team"), rendered.index("After."))

    def test_zensical_extracts_awakener_teams_for_the_guide_template(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lib" / "handbook" / "awakeners" / "chaos" / "example.md"
            source.parent.mkdir(parents=True)
            document = (
                self.AWAKENER_GUIDE
                + f"Before.\n\n```team\n{RENDERABLE_TEAM}```\n\nAfter.\n"
            )
            source.write_text(document, encoding="utf-8")

            import zensical.config as zensical_config
            from zensical.markdown.render import render

            previous_config = zensical_config._CONFIG
            try:
                with self.prepared_temp_project(root, document):
                    awakeners.prepare_awakeners()
                    zensical_config.parse_zensical_config(
                        str(awakeners.GENERATED_CONFIG)
                    )
                    rendered = render(
                        document,
                        "handbook/awakeners/chaos/example.md",
                        "/handbook/awakeners/chaos/example/",
                    )
            finally:
                zensical_config._CONFIG = previous_config

        self.assertNotIn("mythag-team", rendered["content"])
        self.assertEqual(len(rendered["meta"]["mythag_teams"]), 1)
        self.assertIn("mythag-team", rendered["meta"]["mythag_teams"][0])
        self.assertLess(
            rendered["content"].index("Before."),
            rendered["content"].index("After."),
        )

    def test_awakener_template_places_example_teams_after_recommendations(self) -> None:
        from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader

        root = Path(__file__).resolve().parents[1]
        partials = {
            f"partials/{name}.html": ""
            for name in ("actions", "tags", "source-file", "feedback", "comments")
        }
        environment = Environment(
            loader=ChoiceLoader(
                [
                    DictLoader(
                        {"main.html": "{% block content %}{% endblock %}", **partials}
                    ),
                    FileSystemLoader(root / "overrides"),
                ]
            ),
            autoescape=False,
        )
        guide = SimpleNamespace(
            tagline="",
            roles=[],
            ranks=SimpleNamespace(dps=[], support=[]),
            stopping_points=[],
            builds=[
                SimpleNamespace(
                    name="Example Build",
                    covenants=[],
                    covenants_note=None,
                    wheels=SimpleNamespace(early_game=[], astral_reign=[]),
                )
            ],
            suggested_posses=[],
            suggested_posses_note="Any",
            works_well_with=[],
            works_well_with_note="Anyone",
        )
        page = SimpleNamespace(
            content="",
            meta=SimpleNamespace(
                title="Example",
                awakener=guide,
                mythag_teams=['<section id="example-team"></section>'],
            ),
        )
        assets = SimpleNamespace(
            portraits={"Example": SimpleNamespace(image="/portrait.png")},
            covenants={},
            wheels={},
            posses={},
            awakeners={},
        )
        rendered = environment.get_template("awakeners/awakener.html").render(
            page=page,
            config=SimpleNamespace(extra=SimpleNamespace(content_assets=assets)),
        )

        self.assertLess(
            rendered.index('id="build-1"'), rendered.index('id="recommendations"')
        )
        self.assertLess(
            rendered.index('id="recommendations"'),
            rendered.index('id="example-team"'),
        )


if __name__ == "__main__":
    unittest.main()
