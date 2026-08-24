import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from mythag_site import awakeners


ROOT = Path(__file__).resolve().parents[1]


class AwakenerIndexParser(HTMLParser):
    def __init__(self, guide_ids: set[str]) -> None:
        super().__init__()
        self.guide_ids = guide_ids
        self.cards: dict[str, dict[str, str]] = {}
        self.card_ids: list[str] = []
        self.document_ids: set[str] = set()
        self.toc_hrefs: set[str] = set()
        self._active_card: str | None = None
        self._active_label: list[str] = []
        self._secondary_toc_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {key: value or "" for key, value in attrs}
        element_id = values.get("id")
        if element_id:
            self.document_ids.add(element_id)

        classes = set(values.get("class", "").split())
        if tag == "nav" and (
            self._secondary_toc_depth or "md-nav--secondary" in classes
        ):
            self._secondary_toc_depth += 1
        if (
            tag == "a"
            and self._secondary_toc_depth
            and values.get("href", "").startswith("#")
        ):
            self.toc_hrefs.add(values["href"])
        if tag == "a" and element_id in self.guide_ids:
            self._active_card = element_id
            self._active_label = []
            self.card_ids.append(element_id)
            self.cards[element_id] = {"href": values.get("href", "")}
        elif tag == "img" and self._active_card is not None:
            self.cards[self._active_card].update(values)

    def handle_data(self, data: str) -> None:
        if self._active_card is not None:
            self._active_label.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._active_card is not None:
            self.cards[self._active_card]["label"] = "".join(
                self._active_label
            ).strip()
            self._active_card = None
            self._active_label = []
        elif tag == "nav" and self._secondary_toc_depth:
            self._secondary_toc_depth -= 1


class AwakenerContentTests(unittest.TestCase):
    def test_rendered_index_links_every_guide(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            generated_fd, generated_name = tempfile.mkstemp(
                prefix=".test-generated-", suffix=".toml", dir=ROOT
            )
            os.close(generated_fd)
            generated_config = Path(generated_name)
            try:
                with patch.object(awakeners, "GENERATED_CONFIG", generated_config):
                    guides = awakeners.prepare_awakeners()
                    generated = generated_config.read_text(encoding="utf-8")
                    site_dir = Path(temporary).relative_to(ROOT).as_posix()
                    generated = generated.replace(
                        'docs_dir = "lib"\n',
                        f'docs_dir = "lib"\nsite_dir = "{site_dir}"\n',
                        1,
                    )
                    generated_config.write_text(generated, encoding="utf-8")
                    command = [
                        sys.executable,
                        "-m",
                        "zensical",
                        "build",
                        "--clean",
                        "--config-file",
                        str(generated_config),
                    ]
                    try:
                        subprocess.run(
                            command,
                            cwd=ROOT,
                            check=True,
                            capture_output=True,
                            text=True,
                            timeout=120,
                        )
                    except subprocess.CalledProcessError as error:
                        self.fail(
                            "Zensical build failed\n"
                            f"stdout:\n{error.stdout}\n"
                            f"stderr:\n{error.stderr}"
                        )
                    except subprocess.TimeoutExpired as error:
                        self.fail(f"Zensical build exceeded {error.timeout}s")
                    config = tomllib.loads(generated_config.read_text(encoding="utf-8"))
                    index = config["project"]["extra"]["awakener_index"]
                    guide_ids = {guide.slug for guide in guides}
                    html = (
                        Path(temporary) / "handbook" / "awakeners" / "index.html"
                    ).read_text(encoding="utf-8")
            finally:
                generated_config.unlink(missing_ok=True)

        parser = AwakenerIndexParser(guide_ids)
        parser.feed(html)

        self.assertEqual(set(parser.cards), guide_ids)
        self.assertEqual(len(parser.card_ids), len(guide_ids))
        expected_toc = {
            *(f"#{guide_id}" for guide_id in guide_ids),
            *(f"#{group_id}" for group_id in index["group"]),
        }
        self.assertTrue(expected_toc <= parser.toc_hrefs)
        self.assertTrue(
            all(href.removeprefix("#") in parser.document_ids for href in expected_toc)
        )
        self.assertTrue(
            all(
                href.removeprefix("#") in parser.document_ids
                for href in parser.toc_hrefs
            )
        )

        for guide in guides:
            with self.subTest(guide=guide.slug):
                card = parser.cards[guide.slug]
                expected = index["guide"][guide.slug]
                self.assertEqual(card["href"], expected["url"])
                self.assertEqual(card["label"], expected["label"])
                self.assertEqual(card["src"], expected["image"])


if __name__ == "__main__":
    unittest.main()
