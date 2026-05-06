from security.classifier.cvss_scorer import CVSSScorer
import unittest


class TestCVSSScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = CVSSScorer()

    def test_cvss_min_score(self):
        # No targets → overall_cvss should be 0
        result = self.scorer.score_targets([])
        self.assertEqual(result["overall_cvss"], 0.0)
        self.assertEqual(result["overall_severity"], "NONE")

    def test_cvss_max_score(self):
        targets = [
            {
                "function": "withdraw",
                "vulnerability": "reentrancy",
                "cvss": 9.8,
                "severity": "CRITICAL",
            }
        ]
        result = self.scorer.score_targets(targets)
        self.assertLessEqual(result["overall_cvss"], 10.0)
        self.assertGreater(result["overall_cvss"], 0)

    def test_cvss_mid_score(self):
        targets = [
            {
                "function": "transfer",
                "vulnerability": "overflow",
                "cvss": 5.0,
                "severity": "MEDIUM",
            }
        ]
        result = self.scorer.score_targets(targets)
        self.assertGreater(result["overall_cvss"], 0)
        self.assertLess(result["overall_cvss"], 10)
        self.assertIn("details", result)


if __name__ == "__main__":
    unittest.main()
