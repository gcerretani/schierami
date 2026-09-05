import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from tools.build_release import build
from tools.check_project import ROOT, check


class ProjectTests(unittest.TestCase):
    def test_repository_checks(self):
        data = check(ROOT)
        self.assertEqual(data["name"], "schierami")

    def test_examples_are_valid_json(self):
        base = ROOT / "skills/schierami"
        for path in list((base / "examples").glob("*.json")) + list((base / "schemas").glob("*.json")):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))

    def test_release_archives_are_reproducible_and_scoped(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a = build(ROOT, Path(first))
            b = build(ROOT, Path(second))
            for key in ("skill", "plugin"):
                self.assertEqual(
                    hashlib.sha256(a[key].read_bytes()).digest(),
                    hashlib.sha256(b[key].read_bytes()).digest(),
                )
            with zipfile.ZipFile(a["skill"]) as archive:
                names = set(archive.namelist())
                self.assertIn("schierami/SKILL.md", names)
                self.assertIn("schierami/LICENSE", names)
                self.assertIn("schierami/VERSION", names)
                self.assertFalse(any("/tests/" in name for name in names))
                self.assertFalse(any(name.startswith("docs/") for name in names))
            with zipfile.ZipFile(a["plugin"]) as archive:
                names = set(archive.namelist())
                self.assertIn(".codex-plugin/plugin.json", names)
                self.assertIn("skills/schierami/SKILL.md", names)
                self.assertIn("LICENSE", names)
                self.assertFalse(any(name.startswith("tests/") for name in names))
                self.assertFalse(any(name.startswith("tools/") for name in names))


if __name__ == "__main__":
    unittest.main()
