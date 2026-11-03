from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class ArtifactInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.action = yaml.safe_load((ROOT / "action.yml").read_text(encoding="utf-8"))
        cls.upload = next(
            step for step in cls.action["runs"]["steps"]
            if step["name"] == "Upload artifact"
        )

    def upload_inputs(self, supplied=None):
        inputs = {
            name: spec.get("default", "")
            for name, spec in self.action["inputs"].items()
        }
        inputs.update(supplied or {})
        values = {}
        for name, value in self.upload["with"].items():
            if isinstance(value, str) and value.startswith("${{"):
                expression = re.fullmatch(r"\$\{\{ inputs\.(\w+) \}\}", value)
                self.assertIsNotNone(expression, "Expected direct input forwarding")
                values[name] = inputs[expression.group(1)]
            else:
                values[name] = value
        return values

    def test_defaults_preserve_existing_behavior(self):
        self.assertEqual(self.upload_inputs(), {
            "name": "results.sarif",
            "path": "results.sarif",
            "overwrite": "true",
        })
        for name in ("artifact_name", "artifact_overwrite"):
            self.assertIs(self.action["inputs"][name]["required"], False)
            self.assertIsInstance(self.action["inputs"][name]["default"], str)

    def test_inputs_are_forwarded_without_truthiness_fallbacks(self):
        self.assertEqual(self.upload["with"]["name"], "${{ inputs.artifact_name }}")
        self.assertEqual(self.upload["with"]["overwrite"], "${{ inputs.artifact_overwrite }}")

    def test_custom_name_keeps_default_overwrite(self):
        values = self.upload_inputs({"artifact_name": "bandit-api-python39"})
        self.assertEqual(values["name"], "bandit-api-python39")
        self.assertEqual(values["overwrite"], "true")
        self.assertEqual(values["path"], "results.sarif")

    def test_overwrite_can_be_disabled(self):
        values = self.upload_inputs({"artifact_overwrite": "false"})
        self.assertEqual(values["overwrite"], "false")
        self.assertEqual(values["name"], "results.sarif")

    def test_explicit_name_and_overwrite_values(self):
        for overwrite in ("true", "false"):
            with self.subTest(overwrite=overwrite):
                values = self.upload_inputs({
                    "artifact_name": "Bandit API scan",
                    "artifact_overwrite": overwrite,
                })
                self.assertEqual(values["name"], "Bandit API scan")
                self.assertEqual(values["overwrite"], overwrite)
                self.assertEqual(values["path"], "results.sarif")

    def test_code_scanning_path_is_unchanged(self):
        sarif = next(
            step for step in self.action["runs"]["steps"]
            if step["name"] == "Upload SARIF file"
        )
        self.assertEqual(sarif["with"]["sarif_file"], "results.sarif")

    def test_action_dependencies_remain_sha_pinned(self):
        for step in self.action["runs"]["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"@[a-f0-9]{40}$")


if __name__ == "__main__":
    unittest.main()
