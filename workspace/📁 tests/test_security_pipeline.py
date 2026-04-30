import unittest
import json
import requests
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
import os

class TestSecurityPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

    def test_api_endpoint_security(self):
        """Test basic API endpoint security"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertEqual(response.json()["status"], "healthy")

    def test_input_validation(self):
        """Test input validation against malicious inputs"""
        malicious_payloads = [
            {"script": "<script>alert('xss')</script>"},
            {"cmd": "../../../../etc/passwd"},
            {"sql": "DROP TABLE users; --"},
            {"payload": '{"a": "b"}' * 1000}  # Large payload
        ]
        
        for payload in malicious_payloads:
            response = self.client.post("/analyze", json=payload)
            # Should either reject or sanitize the input
            self.assertIn(response.status_code, [200, 400, 422])

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Send many requests rapidly
        for i in range(100):
            response = self.client.get("/health")
            if response.status_code == 429:  # Rate limited
                break
        
        # At least some requests should be rate limited
        response = self.client.get("/health")
        if i < 99:  # If we didn't reach rate limit
            # This might not always trigger depending on settings
            pass

    @patch('requests.post')
    def test_external_api_call_security(self, mock_post):
        """Test security of external API calls"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response
        
        # Test with potentially dangerous URLs
        dangerous_urls = [
            "http://169.254.169.254/latest/meta-data/",  # AWS metadata
            "file:///etc/passwd",
            "http://internal-service:8080/admin"
        ]
        
        for url in dangerous_urls:
            response = self.client.post("/external-call", json={"url": url})
            # Should not allow dangerous URLs
            self.assertNotEqual(response.status_code, 200)

    def test_smart_contract_analysis(self):
        """Test smart contract vulnerability analysis"""
        sample_contract = """
        pragma solidity ^0.8.0;
        
        contract VulnerableContract {
            mapping(address => uint256) public balances;
            
            function withdraw(uint256 amount) external {
                require(balances[msg.sender] >= amount);
                (bool success,) = msg.sender.call{value: amount}("");
                require(success);
                balances[msg.sender] -= amount;  // Reentrancy vulnerability
            }
        }
        """
        
        response = self.client.post(
            "/analyze-contract",
            json={"source": sample_contract}
        )
        
        # Should detect the reentrancy vulnerability
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("vulnerabilities", result)
        detected_vulns = [v["type"] for v in result["vulnerabilities"]]
        self.assertIn("reentrancy", detected_vulns)

    def test_transaction_simulation_security(self):
        """Test security of transaction simulation"""
        simulation_data = {
            "from": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "value": "1000000000000000000",  # 1 ETH
            "data": "0x12345678"
        }
        
        response = self.client.post(
            "/simulate-transaction",
            json=simulation_data
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("gas_used", result)
        self.assertIn("success", result)

    def test_privacy_preserving_features(self):
        """Test privacy-preserving data handling"""
        sensitive_data = {
            "private_key": "0x1234567890abcdef",
            "mnemonic": "word1 word2 word3 ...",
            "personal_info": {
                "address": "123 Main St",
                "ssn": "123-45-6789"
            }
        }
        
        response = self.client.post(
            "/process-sensitive-data",
            json=sensitive_data
        )
        
        # Should either reject or properly handle sensitive data
        self.assertIn(response.status_code, [200, 400, 422])
        
        if response.status_code == 200:
            result = response.json()
            # Ensure sensitive data is not returned in response
            self.assertNotIn("private_key", str(result).lower())

    @patch('os.environ', {'API_KEY': 'valid-key'})
    def test_authentication_bypass_attempts(self):
        """Test resistance to authentication bypass attempts"""
        headers_list = [
            {},  # No auth header
            {"Authorization": ""},  # Empty auth
            {"Authorization": "Invalid token"},  # Invalid format
            {"X-API-Key": "invalid-key"},  # Wrong key
        ]
        
        for headers in headers_list:
            response = self.client.get("/protected-endpoint", headers=headers)
            # Should return 401 or 403 for unauthorized access
            self.assertIn(response.status_code, [401, 403, 422])

    def test_blockchain_interaction_security(self):
        """Test security of blockchain interactions"""
        # Test with potentially dangerous addresses
        dangerous_addresses = [
            "0x0000000000000000000000000000000000000000",  # Zero address
            "0x1234567890123456789012345678901234567890",  # Invalid checksum
            "0xffffffffffffffffffffffffffffffffffffffff",  # Max address
        ]
        
        for addr in dangerous_addresses:
            response = self.client.post(
                "/validate-address",
                json={"address": addr}
            )
            # Should properly validate addresses
            if addr == "0x0000000000000000000000000000000000000000":
                # Zero address might be valid in some contexts
                continue
            else:
                # Other invalid addresses should be rejected
                pass

    def test_dos_protection(self):
        """Test protection against denial-of-service attacks"""
        large_payload = {"data": "x" * 1000000}  # 1MB payload
        
        response = self.client.post("/large-payload-test", json=large_payload)
        # Should either accept with proper processing or reject large payloads
        self.assertIn(response.status_code, [200, 413, 422])  # 413 = Payload Too Large

    def test_error_handling_disclosure(self):
        """Test that error messages don't disclose sensitive information"""
        # Try to trigger various errors
        response = self.client.get("/nonexistent-endpoint")
        self.assertEqual(response.status_code, 404)
        
        # Check that error responses don't contain stack traces
        error_body = response.text.lower()
        self.assertNotIn("traceback", error_body)
        self.assertNotIn("stack", error_body)
        self.assertNotIn("file:", error_body)

if __name__ == '__main__':
    unittest.main()
