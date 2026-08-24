from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from mythag_site import build


class ImageUrlTests(unittest.TestCase):
    def test_caps_only_wheel_delivery_assets_at_640_pixels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            images = Path(temporary) / "images"
            wheel = images / "wheels" / "wheel.png"
            awakener = images / "awakeners" / "awakener.png"
            wheel.parent.mkdir(parents=True)
            awakener.parent.mkdir(parents=True)
            Image.new("RGBA", (430, 872), (255, 0, 0, 128)).save(wheel)
            Image.new("RGBA", (430, 872), (0, 0, 255, 128)).save(awakener)

            with patch.object(build, "SOURCE_IMAGES", images):
                wheel_avif = Path(temporary) / "wheel.avif"
                awakener_avif = Path(temporary) / "awakener.avif"
                build.encode_cached(wheel, wheel_avif)
                build.encode_cached(awakener, awakener_avif)
                self.assertFalse(build.encode_cached(wheel, wheel_avif))

            with Image.open(wheel_avif) as converted:
                self.assertEqual(converted.size, (316, 640))
            with Image.open(awakener_avif) as converted:
                self.assertEqual(converted.size, (430, 872))

            wheel_avif.write_bytes(b"corrupt")
            with patch.object(build, "SOURCE_IMAGES", images):
                build.encode_cached(wheel, wheel_avif)
            self.assertTrue(build.is_valid_avif(wheel_avif))

            site = Path(temporary) / "site"
            site_wheel = site / "images" / "wheels" / "wheel.png"
            site_wheel.parent.mkdir(parents=True)
            Image.new("RGBA", (430, 872), (255, 0, 0, 128)).save(site_wheel)
            page = site / "index.html"
            page.write_text('<img src="/images/wheels/wheel.png">', encoding="utf-8")
            with (
                patch.object(build, "SOURCE_IMAGES", images),
                patch.object(build, "SITE_ROOT", site),
            ):
                build.encode_cached(wheel, site_wheel.with_suffix(".avif"))
                build.rewrite_html_images()
            rewritten = page.read_text(encoding="utf-8")
            self.assertIn('src="/images/wheels/wheel.avif"', rewritten)
            self.assertIn('width="316"', rewritten)
            self.assertIn('height="640"', rewritten)

    def test_rewrites_root_and_relative_image_urls_only_when_avif_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary)
            page = site / "handbook" / "awakeners" / "index.html"
            avif = site / "images" / "awakener.avif"
            page.parent.mkdir(parents=True)
            avif.parent.mkdir(parents=True)
            avif.write_bytes(b"avif")

            with patch.object(build, "SITE_ROOT", site):
                self.assertEqual(
                    build.avif_url("/images/awakener.png", page),
                    "/images/awakener.avif",
                )
                self.assertEqual(
                    build.avif_url("../../images/awakener.png", page),
                    "../../images/awakener.avif",
                )
                self.assertIsNone(build.avif_url("/images/missing.png", page))
                self.assertIsNone(
                    build.avif_url("https://example.com/awakener.png", page)
                )

    def test_rewrites_img_elements_without_touching_other_src_attributes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary)
            page = site / "index.html"
            avif = site / "images" / "awakener.avif"
            avif.parent.mkdir(parents=True)
            Image.new("RGBA", (400, 200)).save(avif.with_suffix(".png"))
            Image.new("RGBA", (200, 100)).save(avif, "AVIF")
            page.write_text(
                '<script src="/images/awakener.png"></script>'
                '<a class="glightbox" data-type="image" '
                'href="/images/awakener.png">'
                '<img src="/images/awakener.png" alt="Awakener"></a>'
                '<img src="/images/awakener.png" alt="Small" width="100">'
                '<img src="/images/awakener.png" alt="Decimal" width="117.95">',
                encoding="utf-8",
            )

            with patch.object(build, "SITE_ROOT", site):
                build.rewrite_html_images()

            rewritten = page.read_text(encoding="utf-8")
            self.assertIn('<script src="/images/awakener.png">', rewritten)
            self.assertIn('href="/images/awakener.avif"', rewritten)
            self.assertIn('src="/images/awakener.avif"', rewritten)
            self.assertIn('width="200"', rewritten)
            self.assertIn('height="100"', rewritten)
            self.assertIn('width="100"', rewritten)
            self.assertIn('height="50"', rewritten)
            self.assertIn('width="117.95"', rewritten)
            self.assertIn('height="59"', rewritten)


class PngPruningTests(unittest.TestCase):
    def make_delivery_pair(self, source: Path, built_png: Path) -> int:
        source.parent.mkdir(parents=True, exist_ok=True)
        built_png.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (32, 16), (255, 0, 0, 128)).save(source)
        built_png.write_bytes(source.read_bytes())
        Image.new("RGBA", (32, 16), (255, 0, 0, 128)).save(
            built_png.with_suffix(".avif"), "AVIF"
        )
        return built_png.stat().st_size

    def test_refuses_all_pruning_when_deployable_text_references_a_candidate(self) -> None:
        references = {
            "index.html": '<a href="/images/example.png">image</a>',
            "entity.html": '<img src="/images/example&#46;png">',
            "styles.css": 'body { background: url("/images/example.png"); }',
            "app.js": 'const image = "/images/example.png";',
            "site.webmanifest": '{"icon": "/images/example.png"}',
        }
        for filename, reference in references.items():
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                images = root / "source-images"
                site = root / "site"
                built_png = site / "images" / "example.png"
                self.make_delivery_pair(images / "example.png", built_png)
                (site / filename).write_text(reference, encoding="utf-8")

                with (
                    patch.object(build, "SOURCE_IMAGES", images),
                    patch.object(build, "SITE_ROOT", site),
                ):
                    with self.assertRaises(RuntimeError) as context:
                        build.verify_and_prune_source_pngs()

                self.assertTrue(built_png.is_file())
                if filename == "index.html":
                    self.assertIn(filename, str(context.exception))

    def test_prunes_only_unreferenced_source_mapped_pngs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            images = root / "source-images"
            site = root / "site"
            built_png = site / "images" / "example.png"
            self.make_delivery_pair(images / "example.png", built_png)
            logo_png = site / "images" / "logo.png"
            self.make_delivery_pair(images / "logo.png", logo_png)
            theme_png = site / "assets" / "images" / "favicon.png"
            theme_png.parent.mkdir(parents=True)
            theme_png.write_bytes(b"theme")
            (site / "index.html").write_text(
                '<link rel="icon" href="/images/logo.png">', encoding="utf-8"
            )

            with (
                patch.object(build, "SOURCE_IMAGES", images),
                patch.object(build, "SITE_ROOT", site),
            ):
                build.verify_and_prune_source_pngs()

            self.assertFalse(built_png.exists())
            self.assertTrue(built_png.with_suffix(".avif").is_file())
            self.assertTrue(logo_png.is_file())
            self.assertTrue(theme_png.is_file())

    def test_refuses_pruning_when_delivery_avif_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            images = root / "source-images"
            site = root / "site"
            built_png = site / "images" / "example.png"
            self.make_delivery_pair(images / "example.png", built_png)
            built_png.with_suffix(".avif").write_bytes(b"corrupt")

            with (
                patch.object(build, "SOURCE_IMAGES", images),
                patch.object(build, "SITE_ROOT", site),
            ):
                with self.assertRaises(RuntimeError):
                    build.verify_and_prune_source_pngs()

            self.assertTrue(built_png.is_file())


class AbbreviationTests(unittest.TestCase):
    def test_expands_template_text_without_touching_existing_markup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            site = root / "site"
            page = site / "handbook" / "awakeners" / "chaos" / "24" / "index.html"
            abbreviations = root / "abbreviations.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<div class="awakener-guide" data-abbreviations>'
                '<p title="Tier">Using Action at Tier with Awakener.</p>'
                '<p><abbr title="existing">Tier</abbr> and <code>Action</code></p>'
                '</div><p>Tier outside the guide.</p>',
                encoding="utf-8",
            )
            abbreviations.write_text(
                '*[Tier]: Example tier.\n'
                '*[Action]: Example action.\n'
                '*[Awakener]: Example character.\n'
                '*[Using]: Example use.\n',
                encoding="utf-8",
            )

            with (
                patch.object(build, "SITE_ROOT", site),
                patch.object(build, "ABBREVIATIONS", abbreviations),
            ):
                build.expand_html_abbreviations()
                self.assertEqual(build.expand_html_abbreviations(), (0, 0))

            rewritten = page.read_text(encoding="utf-8")
            self.assertIn(
                '<abbr title="Example use.">Using</abbr>',
                rewritten,
            )
            self.assertIn('<abbr title="Example tier.">Tier</abbr>', rewritten)
            self.assertIn('<abbr title="Example action.">Action</abbr>', rewritten)
            self.assertIn('<abbr title="Example character.">Awakener</abbr>', rewritten)
            self.assertIn('<p title="Tier">', rewritten)
            self.assertIn('<abbr title="existing">Tier</abbr>', rewritten)
            self.assertIn('<code>Action</code>', rewritten)
            self.assertIn('<p>Tier outside the guide.</p>', rewritten)


if __name__ == "__main__":
    unittest.main()
