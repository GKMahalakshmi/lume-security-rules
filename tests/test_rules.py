import os
import re
import json
import yaml
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(BASE_DIR, "rules")
FIXTURES_DIR = os.path.join(BASE_DIR, "tests", "fixtures")

REQUIRED_FIELDS = [
    "id",
    "name",
    "description",
    "category",
    "severity",
    "confidence",
    "validation_status",
    "target",
    "detection_logic",
    "known_limitations",
    "test_fixtures"
]

def load_all_rules():
    rules = {}
    for root, _, files in os.walk(RULES_DIR):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                rule_path = os.path.join(root, file)
                with open(rule_path, "r", encoding="utf-8") as f:
                    rule_data = yaml.safe_load(f)
                    rules[rule_data["id"]] = (rule_data, rule_path)
    return rules

def load_all_fixtures():
    fixtures = []
    for root, _, files in os.walk(FIXTURES_DIR):
        for file in files:
            if file.endswith(".json"):
                fixture_path = os.path.join(root, file)
                with open(fixture_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    fixtures.append((data, fixture_path))
    return fixtures

def evaluate_rule(rule, text, target):
    if rule.get("target") != target:
        return False

    logic = rule.get("detection_logic", {})
    patterns = logic.get("patterns", [])
    negative_patterns = logic.get("negative_patterns", [])

    # Check negative/exclusion patterns first
    for neg_pat in negative_patterns:
        if re.search(neg_pat, text, re.IGNORECASE):
            return False

    # Check positive patterns
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True

    return False


class TestRuleSchemaAndIntegrity(unittest.TestCase):
    def setUp(self):
        self.rules = load_all_rules()

    def test_rules_discovered(self):
        self.assertGreater(len(self.rules), 0, "No rules discovered in rules/ directory.")

    def test_rules_schema_compliance(self):
        for rule_id, (rule, file_path) in self.rules.items():
            with self.subTest(rule_id=rule_id, file=file_path):
                for field in REQUIRED_FIELDS:
                    self.assertIn(field, rule, f"Rule {rule_id} missing required field: {field}")

                self.assertIn(
                    rule["validation_status"],
                    ["experimental / unvalidated", "testing", "validated", "production"],
                    f"Invalid validation_status for rule {rule_id}"
                )
                self.assertIn(
                    rule["severity"],
                    ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                    f"Invalid severity for rule {rule_id}"
                )
                self.assertIn(
                    rule["confidence"],
                    ["LOW", "MEDIUM", "HIGH"],
                    f"Invalid confidence for rule {rule_id}"
                )
                self.assertIn(
                    rule["target"],
                    ["prompt", "response"],
                    f"Invalid target for rule {rule_id}"
                )
                self.assertIsInstance(
                    rule["known_limitations"],
                    list,
                    f"known_limitations must be a list in {rule_id}"
                )
                self.assertGreater(
                    len(rule["known_limitations"]),
                    0,
                    f"known_limitations must not be empty in {rule_id}"
                )


class TestRuleDetectionValidation(unittest.TestCase):
    def setUp(self):
        self.rules = load_all_rules()
        self.fixtures = load_all_fixtures()

    def test_fixtures_discovered(self):
        self.assertGreater(len(self.fixtures), 0, "No test fixtures found in tests/fixtures/")

    def test_fixture_execution(self):
        positive_count = 0
        negative_count = 0

        for fixture, fix_path in self.fixtures:
            rule_id = fixture["rule_id"]
            self.assertIn(rule_id, self.rules, f"Fixture references unknown rule_id: {rule_id} in {fix_path}")

            rule, _ = self.rules[rule_id]
            expected = fixture["expected_match"]
            text = fixture["text"]
            target = fixture["target"]

            result = evaluate_rule(rule, text, target)

            if expected:
                positive_count += 1
                self.assertTrue(
                    result,
                    f"[FALSE NEGATIVE] Rule {rule_id} failed to match positive attack fixture {fixture['fixture_id']}: '{text}'"
                )
            else:
                negative_count += 1
                self.assertFalse(
                    result,
                    f"[FALSE POSITIVE] Rule {rule_id} incorrectly flagged benign fixture {fixture['fixture_id']}: '{text}'"
                )

        print(f"\nRule Validation Results: {positive_count} positive attacks caught, {negative_count} benign fixtures correctly cleared (0 false positives).")


if __name__ == "__main__":
    unittest.main()
