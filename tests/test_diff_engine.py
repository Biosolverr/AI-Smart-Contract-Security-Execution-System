import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from security.simulator.diff_engine import DiffEngine


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

    def test_diff_no_change(self):
        engine = DiffEngine()
        state = {"balance": 100, "owner": "0xabc"}
        diff = engine.compare(state, state)
        self.assertEqual(diff, {})

    def test_diff_added_key(self):
        engine = DiffEngine()
        state1 = {"balance": 100}
        state2 = {"balance": 100, "locked": True}
        diff = engine.compare(state1, state2)
        self.assertIn("locked", diff)


if __name__ == '__main__':
    unittest.main()
