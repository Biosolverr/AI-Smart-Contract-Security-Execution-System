from analysis.parser.solidity_ast_parser import SolidityASTParser
import unittest


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


class TestSolidityParser(unittest.TestCase):
    def setUp(self):
        self.parser = SolidityASTParser()

    def test_parse_simple(self):
        result = self.parser.parse(SIMPLE_CONTRACT)
        self.assertIsNotNone(result)
        # Parser returns a dict with "functions" key
        self.assertIn("functions", result)
        func_names = [f["name"] for f in result["functions"]]
        self.assertIn("set", func_names)

    def test_parse_complex(self):
        result = self.parser.parse(COMPLEX_CONTRACT)
        self.assertIsNotNone(result)
        self.assertIn("functions", result)
        func_names = [f["name"] for f in result["functions"]]
        self.assertIn("withdraw", func_names)
        # mapping type should appear in state_vars
        types = [v["type"] for v in result.get("state_vars", [])]
        self.assertTrue(any("mapping" in t for t in types))


if __name__ == "__main__":
    unittest.main()
