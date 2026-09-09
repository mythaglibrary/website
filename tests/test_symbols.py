import tempfile
import unittest
from pathlib import Path

from markdown import Markdown

from mythag_site.symbols import SymbolValidationError, SymbolsExtension, load_symbols


class SymbolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "content").mkdir()
        (self.root / "lib/images").mkdir(parents=True)
        (self.root / "lib/images/icon.png").write_bytes(b"test")
        self.path = self.root / "content/symbols.yaml"
        self.path.write_text("custom: {label: Custom, icon: /images/icon.png}\n", encoding="utf-8")

    def render(self, text):
        return Markdown(extensions=["fenced_code", SymbolsExtension(root=str(self.root))]).convert(text)

    def test_authored_names_and_protected_examples(self):
        result = self.render(':custom: `:unknown:`\n\n```\n:unknown:\n```\n\n[link](https://example.com/:unknown:)\n\n<span title=":unknown:">:unknown:</span>')
        self.assertEqual(result.count('class="mythag-symbol"'), 1)
        self.assertIn('<code>:unknown:</code>', result)
        self.assertIn('https://example.com/:unknown:', result)
        self.assertIn('<span title=":unknown:">:unknown:</span>', result)
        self.path.write_text('custom: {label: Custom, icon: /images/icon.png, width: 18}\n', encoding='utf-8')
        self.assertEqual(load_symbols(self.root)['custom']['width'], 18)
        with self.assertRaisesRegex(SymbolValidationError, 'unknown symbol :custm:.*custom'):
            self.render(':custm:')

    def test_invalid_registry_and_missing_assets(self):
        for source in (
            'custom: {}\n',
            *[f'custom: {{label: Custom, icon: /images/icon.png, width: {width}}}\n'
              for width in ('0', '-1', 'true', '12px', '1.5')],
            'heart: {label: Custom, icon: /images/icon.png}\n',
            'custom: {label: Custom, icon: /images/missing.png}\n',
            'custom: {}\ncustom: {}\n',
        ):
            with self.subTest(source=source):
                self.path.write_text(source, encoding="utf-8")
                with self.assertRaises(SymbolValidationError):
                    load_symbols(self.root)


if __name__ == "__main__":
    unittest.main()
