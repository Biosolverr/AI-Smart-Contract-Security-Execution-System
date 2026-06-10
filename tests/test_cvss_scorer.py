import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from security.classifier.cvss_scorer import calculate_cvss_score


class TestCVSSScorer(unittest.TestCase):
    def test_cvss_min_score(self):
        score = calculate_cvss_score(
            attack_vector=0, complexity=0, privileges_required=0,
            user_interaction=0, impact=0
        )
        self.assertTrue(score == 0 or score < 1)

    def test_cvss_max_score(self):
        score = calculate_cvss_score(
            attack_vector=1, complexity=1, privileges_required=1,
            user_interaction=1, impact=1
        )
        self.assertLessEqual(score, 10)

    def test_cvss_mid_score(self):
        score = calculate_cvss_score(
            attack_vector=0.5, complexity=0.5, privileges_required=0.5,
            user_interaction=0.5, impact=0.5
        )
        self.assertGreater(score, 0)
        self.assertLess(score, 10)


if __name__ == '__main__':
    unittest.main()
