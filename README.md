[README.md](https://github.com/user-attachments/files/27247288/README.md)
# GenRoute AI
**Intelligent Intent Routing on GenLayer Blockchain**

GenRoute AI is an intelligent intent routing system built on the GenLayer blockchain platform. It analyzes user requests (e.g., "Transfer 500 USDC to Alice"), determines which executor should handle the operation (financial, audit, social, or consensus), and routes it to the appropriate module. The system uses AI for classification, learns from past decisions, applies consensus when uncertain, and is protected against attacks. Created for automating decision-making and secure execution of actions on the blockchain.

## 🛡️ Security Verification

This repository includes two distinct testing suites to verify the robustness of the GenRoute AI:

### 1. Attack Suite (Vulnerability Scanning)
Located in `contracts/tests/attack_suite/`.
- Contains 7 specific attack vectors (Prompt Injection, JSON Injection, Logic Confusion).
- **Goal:** Demonstrate potential risks if protections were absent.
- **Status:** All attacks detected and neutralized.

### 2. Success Proofs (Verification)
Located in `contracts/tests/success_proofs/`.
- Contains cryptographic and logical proofs that the contract behaves correctly under attack.
- Includes `SECURITY_PROOFS_REPORT.json` with detailed execution traces.
- **Goal:** Provide undeniable evidence that the security layers hold.

## 🚀 Quick Start

### Run Attack Simulation
```bash
cd contracts/tests/attack_suite
python run_attack_tests.py
