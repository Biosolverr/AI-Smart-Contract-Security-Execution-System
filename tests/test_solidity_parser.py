import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from analysis.parser.solidity_ast_parser import SolidityASTParser


SIMPLE_CONTRACT = """
pragma solidity ^0.8.0;

contract Test {
    uint public value;

    function set(uint _v) public {
        value = _v;
    }
}
"""

COMPLEX_CONTRACT = """
pragma solidity ^0.8.0;

contract Complex {
    mapping(address => uint) balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
"""

REENTRANCY_CONTRACT = """
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint) public balances;

    function withdraw(uint amount) public {
        payable(msg.sender).call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
"""


class TestSolidityParser(unittest.TestCase):
    def setUp(self):
        self.parser = SolidityASTParser()

    def test_parse_simple(self):
        ast = self.parser.parse(SIMPLE_CONTRACT)
        self.assertIsNotNone(ast)
        self.assertIn("contract", str(ast).lower())

    def test_parse_complex(self):
        ast = self.parser.parse(COMPLEX_CONTRACT)
        self.assertIsNotNone(ast)
        self.assertIn("mapping", str(ast).lower())

    def test_parse_returns_functions(self):
        ast = self.parser.parse(SIMPLE_CONTRACT)
        self.assertIn("functions", ast)
        self.assertTrue(len(ast["functions"]) > 0)

    def test_parse_function_name(self):
        ast = self.parser.parse(SIMPLE_CONTRACT)
        names = [f["name"] for f in ast["functions"]]
        self.assertIn("set", names)

    def test_parse_empty(self):
        ast = self.parser.parse("")
        self.assertIsNotNone(ast)
        self.assertEqual(ast["functions"], [])

    def test_reentrancy_detection(self):
        ast = self.parser.parse(REENTRANCY_CONTRACT)
        warnings = ast.get("warnings", [])
        found = any("REENTRANCY" in w.upper() for w in warnings)
        self.assertTrue(found, f"Expected reentrancy warning, got: {warnings}")


if __name__ == '__main__':
    unittest.main()
