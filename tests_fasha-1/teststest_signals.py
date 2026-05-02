from security.classifier.signals import rule_based_score
import unittest

class TestSignals(unittest.TestCase):
    def test_rule_based_low(self):
        score = rule_based_score({"reentrancy": False})
        self.assertGreaterEqual(score, 0)

    def test_rule_based_high(self):
        score = rule_based_score({"reentrancy": True})
        self.assertGreater(score, 0)

if __name__ == '__main__':
    unittest.main()
