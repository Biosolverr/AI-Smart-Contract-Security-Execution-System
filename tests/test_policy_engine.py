import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from security.routing.policy_engine import PolicyEngine


class TestPolicyEngine(unittest.TestCase):
    def test_policy_allow(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "low", "value": 10})
        self.assertIn(decision, ["allow", True])

    def test_policy_block_high_risk(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "high", "value": 1000000})
        self.assertIn(decision, ["block", False])

    def test_policy_block_high_value(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "low", "value": 200_000})
        self.assertEqual(decision, "block")

    def test_policy_warn_medium(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "medium", "value": 500})
        self.assertEqual(decision, "warn")

    def test_policy_edge_zero(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "low", "value": 0})
        self.assertIsNotNone(decision)


if __name__ == '__main__':
    unittest.main()
