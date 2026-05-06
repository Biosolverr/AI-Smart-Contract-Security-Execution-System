from security.simulator.diff_engine import DiffEngine
import unittest


class TestDiffEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DiffEngine()

    def test_diff_empty(self):
        # diff of two identical empty states → no changes
        result = self.engine.diff({}, {})
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

    def test_diff_simple_change(self):
        state1 = {"balances": {"alice": 100}}
        state2 = {"balances": {"alice": 200}}
        result = self.engine.diff(state1, state2)
        # Should report a balance change for alice
        self.assertTrue(any("alice" in entry for entry in result))

    def test_diff_nested(self):
        state1 = {"storage": {"slot0": "0x00"}}
        state2 = {"storage": {"slot0": "0xff"}}
        result = self.engine.diff(state1, state2)
        self.assertTrue(any("slot0" in entry for entry in result))


if __name__ == "__main__":
    unittest.main()
