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
    def test_parse_simple(self):
        parser = SolidityASTParser()
        ast = parser.parse(SIMPLE_CONTRACT)
        self.assertIsNotNone(ast)
        self.assertIn("contract", str(ast).lower())

    def test_parse_complex(self):
        parser = SolidityASTParser()
        ast = parser.parse(COMPLEX_CONTRACT)
        self.assertIsNotNone(ast)
        self.assertIn("mapping", str(ast).lower())

if __name__ == '__main__':
    unittest.main()
