import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from security.pipeline.security_pipeline import SecurityPipeline


VAULT_CONTRACT = """
pragma solidity ^0.8.0;

contract VulnerableVault {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        payable(msg.sender).call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
"""


class TestSecurityPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = SecurityPipeline()

    def test_pipeline_runs(self):
        result = self.pipeline.run("audit contract", VAULT_CONTRACT)
        self.assertIsNotNone(result)

    def test_pipeline_returns_ast(self):
        result = self.pipeline.run("audit", VAULT_CONTRACT)
        self.assertIn("ast", result)
        self.assertIn("functions", result["ast"])

    def test_pipeline_returns_exploits(self):
        result = self.pipeline.run("audit", VAULT_CONTRACT)
        self.assertIn("exploits", result)

    def test_pipeline_returns_graph(self):
        result = self.pipeline.run("audit", VAULT_CONTRACT)
        self.assertIn("graph", result)
        self.assertIn("nodes", result["graph"])
        self.assertIn("edges", result["graph"])

    def test_pipeline_empty_contract(self):
        result = self.pipeline.run("audit", "")
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
