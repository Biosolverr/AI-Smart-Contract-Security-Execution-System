import unittest
from security.classifier.cvss_scorer import CVSSScorer


class TestCVSSScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = CVSSScorer()

    def test_cvss_min_score(self):
        # UNCHECKED_PAYMENT → cvss 5.5 (MEDIUM, самый низкий в EXPLOIT_MAP)
        result = self.scorer.score("UNCHECKED_PAYMENT")
        self.assertGreaterEqual(result.get("cvss", 0), 0.0)
        self.assertLessEqual(result.get("cvss", 0), 6.9)

    def test_cvss_mid_score(self):
        # VALUE_MOVE → cvss 6.5 (MEDIUM)
        result = self.scorer.score("VALUE_MOVE")
        score = result.get("cvss", 0)
        self.assertGreaterEqual(score, 4.0)
        self.assertLessEqual(score, 6.9)

    def test_cvss_max_score(self):
        # REENTRANCY → cvss 9.5 (CRITICAL)
        result = self.scorer.score("REENTRANCY")
        self.assertGreaterEqual(result.get("cvss", 0), 7.0)


if __name__ == "__main__":
    unittest.main()
