"""Tests for check_dependencies.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_dependencies as cd  # noqa: E402

NOW = datetime(2026, 11, 3, tzinfo=timezone.utc)
OLD = (NOW - timedelta(days=900), 40)
APPROVED = "| python | fastapi | 0.1 | 2026-11-03 | plan |\n| npm | react | 19 | 2026-11-03 | plan |\n"


def run(base_files, head_files, lookup):
    files = {cd.APPROVED_FILE: head_files.pop(cd.APPROVED_FILE, "")}
    files.update(head_files)
    return cd.check(
        "BASE",
        lookup=lookup,
        show=lambda base, path: base_files.get(path, ""),
        read=lambda path: files.get(path, ""),
        now=NOW,
    )


class Tests(unittest.TestCase):
    def test_parsers(self):
        self.assertEqual(cd.parse_requirements_in("# c\nFastAPI[all]==1\n-r other\n\nsome_pkg>=2"), {"fastapi", "some-pkg"})
        self.assertEqual(cd.parse_package_json('{"dependencies":{"React":"1"},"devDependencies":{"@x/y":"2"}}'), {"react", "@x/y"})
        pub = "name: a\ndependencies:\n  flutter:\n    sdk: flutter\n  dio: ^5\n# c\ndev_dependencies:\n  flutter_test:\n    sdk: flutter\n  lints: ^3\nflutter:\n  uses-material-design: true\n"
        self.assertEqual(cd.parse_pubspec(pub), {"dio", "lints"})

    def test_unapproved_real_package_fails(self):
        errs, _ = run({}, {"api/requirements.in": "requests\n", cd.APPROVED_FILE: APPROVED}, lambda e, n: OLD)
        self.assertEqual(len(errs), 1)
        self.assertIn("not in", errs[0])

    def test_invented_package_fails(self):
        errs, _ = run({}, {"api/requirements.in": "fastapi\nfastapi-turbo-auth-helper\n", cd.APPROVED_FILE: APPROVED + "| python | fastapi-turbo-auth-helper | 1 | d | p |\n"},
                      lambda e, n: None if n == "fastapi-turbo-auth-helper" else OLD)
        self.assertEqual(len(errs), 1)
        self.assertIn("does not exist", errs[0])

    def test_approved_established_package_passes(self):
        errs, warns = run({}, {"api/requirements.in": "fastapi\n", cd.APPROVED_FILE: APPROVED}, lambda e, n: OLD)
        self.assertEqual((errs, warns), ([], []))

    def test_new_package_warns(self):
        errs, warns = run({}, {"web/package.json": '{"dependencies":{"react":"19"}}', cd.APPROVED_FILE: APPROVED},
                          lambda e, n: (NOW - timedelta(days=3), 1))
        self.assertEqual(errs, [])
        self.assertEqual(len(warns), 2)

    def test_existing_dependency_not_rechecked(self):
        errs, _ = run({"api/requirements.in": "requests\n"}, {"api/requirements.in": "requests\n", cd.APPROVED_FILE: ""}, lambda e, n: OLD)
        self.assertEqual(errs, [])


if __name__ == "__main__":
    unittest.main()
