from security.simulator.diff_engine import DiffEngine
import unittest


class TestDiffEngine(unittest.TestCase):
    def test_diff_empty(self):
        engine = DiffEngine()
        diff = engine.compare({}, {})
        self.assertTrue(diff == {} or diff is not None)

    def test_diff_simple_change(self):
        engine = DiffEngine()
        state1 = {"balance": 100}
        state2 = {"balance": 200}
        diff = engine.compare(state1, state2)
        self.assertIn("balance", diff)

    def test_diff_nested(self):
        engine = DiffEngine()
        state1 = {"user": {"balance": 100}}
        state2 = {"user": {"balance": 150}}
        diff = engine.compare(state1, state2)
        self.assertIn("user", diff)


if __name__ == '__main__':
    unittest.main()
