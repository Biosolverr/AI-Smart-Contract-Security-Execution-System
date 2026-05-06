from security.routing.policy_engine import PolicyEngine
import unittest


class TestPolicyEngine(unittest.TestCase):
    def test_policy_allow(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "low", "value": 10})
        self.assertIn(decision, ["allow", True])

    def test_policy_block(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "high", "value": 1000000})
        self.assertIn(decision, ["block", False])

    def test_policy_edge(self):
        engine = PolicyEngine()
        decision = engine.evaluate({"risk": "medium", "value": 500})
        self.assertIsNotNone(decision)


if __name__ == '__main__':
    unittest.main()
