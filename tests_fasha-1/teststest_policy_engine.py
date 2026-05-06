from security.routing.policy_engine import PolicyEngine
import unittest


class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()

    def test_policy_allow(self):
        # Non-BLOCK decision keeps the original executor
        decision = {"action": "ALLOW"}
        result = self.engine.apply(decision, executor="financial_executor")
        self.assertEqual(result, "financial_executor")

    def test_policy_block(self):
        # BLOCK decision always routes to consensus_executor
        decision = {"action": "BLOCK"}
        result = self.engine.apply(decision, executor="financial_executor")
        self.assertEqual(result, "consensus_executor")

    def test_policy_edge(self):
        # WARN on financial_executor → routes to audit_executor
        decision = {"action": "WARN"}
        result = self.engine.apply(decision, executor="financial_executor")
        self.assertIsNotNone(result)
        self.assertEqual(result, "audit_executor")


if __name__ == "__main__":
    unittest.main()
