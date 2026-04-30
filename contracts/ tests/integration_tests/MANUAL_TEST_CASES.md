[MANUAL_TEST_CASES.md](https://github.com/user-attachments/files/27246617/MANUAL_TEST_CASES.md)
# 🧪 GenRoute Manual Integration Test Cases

This document contains step-by-step instructions for manually testing admin functions, threshold logic, and the contract analysis pipeline using the GenLayer Studio or similar interface.

## ⚙️ Block 1: Threshold Management (`set_threshold`)

| ID | Action | Input Value | Expected Result | Verification Step |
|----|--------|-------------|-----------------|-------------------|
| **T-01** | Set Threshold | `50` | Success | Call `get_threshold()` → returns `50` |
| **T-02** | Min Boundary | `1` | Success | Call `route("any")` → `consensus_used: false` |
| **T-03** | Max Boundary | `99` | Success | Call `route("transfer...")` → `consensus_used: true` |
| **T-04** | Invalid Low | `0` | **Error** | Expect `AssertionError: Threshold must be 1-99` |
| **T-05** | Invalid High | `100` | **Error** | Expect `AssertionError: Threshold must be 1-99` |
| **T-06** | Reset Default | `70` | Success | Restore default behavior |

## 🛠️ Block 2: Executor Registration (`register_executor`)

*Note: Must be called by Owner address.*

| ID | Action | Inputs | Expected Result |
|----|--------|--------|-----------------|
| **E-01** | Register Valid | `name="risk_executor"`, `desc="Handles high-risk..."`, `tier=3`, `boost=8` | Success. Count = 5 |
| **E-02** | Duplicate Name | `name="financial_executor"` | **Error**: `Executor already registered` |
| **E-03** | Short Desc | `desc="short"` | **Error**: `Description too short` |
| **E-04** | Bad Tier (0) | `tier=0` | **Error**: `cost_tier must be 1-3` |
| **E-05** | Bad Tier (4) | `tier=4` | **Error**: `cost_tier must be 1-3` |
| **E-06** | Bad Boost (101)| `boost=101` | **Error**: `cannot exceed 100` |
| **E-07** | Max Boost (100)| `boost=100` | Success. Boundary accepted |
| **E-08** | Empty Name | `name=""` | **Error**: `Name cannot be empty` |

## 📝 Block 3: Outcome Recording (`record_outcome`)

| ID | Action | Inputs | Expected Result |
|----|--------|--------|-----------------|
| **O-01** | Record Success | `key="test_01"`, `exec="social_executor"`, `success=true` | Memory updated |
| **O-02** | Record Failure | `key="test_01"`, `success=false` | Failure count = 1 |
| **O-03** | Repeat Failure | `key="test_01"`, `success=false` | Failure count = 2 |
| **O-07** | Invalid Exec | `exec="fake_exec"` | **Error**: `Unknown executor` |
| **O-08** | Empty Key | `key=""` | **Error**: `key cannot be empty` |

## 🔍 Block 4: Contract Analysis (`analyze_contract`)

### A-01: Safe Contract

**Input Source:**
```python
class SafeVault(gl.Contract):
    owner: Address
    balance: u256
    
    def __init__(self):
        self.owner = gl.message.sender_address
    
    @gl.public.write
    def deposit(self, amount: u256):
        self.balance += amount
