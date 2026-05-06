GenRoute AI
AI-powered intent routing and smart contract security system built on GenLayer.

What is this?
GenRoute is an intelligent middleware that sits between a user's natural language request and blockchain execution. It reads what the user wants, classifies it using LLMs running inside a GenLayer smart contract, routes the request to the right executor, and remembers the result to get smarter over time.
Unlike traditional smart contracts with hardcoded logic, GenRoute dynamically understands intent — and blocks injection attacks before they ever reach the LLM.

Core Contract: FulGenRoute.py
This is the main deployed contract. All testing was performed on this file on GenLayer Testnet.
How routing works
User writes natural language input
        ↓
[Pre-filter] — rule-based injection & uncertainty detection (no LLM)
        ↓
[LLM Classifier] — base64-encoded input → executor + confidence score
        ↓
      confidence ≥ threshold?
       YES              NO
        ↓               ↓
  [Executor]    [consensus_executor fallback]
        ↓
  [commit_route] — deterministic storage write
        ↓
  [routing_memory] — cached for future requests
Public Methods
MethodTypeDescriptionroute(user_input)writeClassifies intent via LLM, returns executor + key. Does NOT write to storage.commit_route(user_input, executor, confidence, source, reason)writePersists routing result to traces and routing_memory. Call after route().analyze_contract(source, label)writeRuns 4-layer AI security pipeline: parse → attack gen → simulate → classify.commit_analyze(source, label, contract_name, risk_score, decision, findings_json, attacks_json)writePersists analysis report to storage. Call after analyze_contract().record_outcome(key, executor, success)writeUpdates routing memory with feedback. Owner-only.register_executor(name, description, cost_tier, confidence_boost)writeAdds new executor. Owner-only.set_threshold(value)writeSets consensus fallback threshold 1-99. Owner-only.get_route_key(user_input)viewReturns the routing_memory key for a given input. Use for record_outcome.get_traces()viewReturns full routing history.get_all_reports()viewReturns list of all security reports.get_report(index)viewReturns full report with findings at given index.get_executors()viewLists all registered executors.get_threshold()viewReturns current consensus threshold.
Why two steps? (route + commit_route)
GenLayer does not persist storage writes from methods that call run_nondet_unsafe (LLM calls). The route() method calls the LLM — so its storage writes are discarded after finalization. commit_route() is a deterministic follow-up that actually saves to the blockchain. This is a GenLayer architecture constraint, not a contract bug.
Same pattern applies to analyze_contract + commit_analyze.

Built-in Executors
ExecutorPurposeCost Tierfinancial_executorPayments, DeFi, token transfers2audit_executorSmart contract security analysis3social_executorDAO governance, proposals, voting1consensus_executorFallback for ambiguous or high-risk requests3
New executors can be added by the owner via register_executor().

Security Features
Pre-filter (rule-based, before LLM)
The contract checks every input against injection and uncertainty patterns before the LLM ever sees it:
pythonINJECTION_PATTERNS = [
    "ignore previous", "override", "bypass", "route to ",
    "executor:", "\"executor\"", "confidence 100", ...
]
UNCERTAINTY_PATTERNS = [
    "or don't", "i'm not sure", "maybe", "whatever", "just do", ...
]
Matched inputs → consensus_executor, source=pre_filter, no LLM call.
Base64 encoding
User input is base64-encoded before being sent to the LLM, with explicit instruction to treat decoded content as untrusted data.
Confidence threshold
If LLM confidence < threshold (default 70%) → consensus_executor fallback.

Repository Structure
AI-Smart-Contract-Security-Execution-System/
├── FulGenRoute.py              # Main contract — deploy this
├── frontend/
│   ├── index.html              # Dashboard UI — open in browser
│   ├── app.js                  # UI logic
│   ├── config.js               # Contract address + RPC config
│   └── dashboard/              # VulnerabilityReport, RiskScoreCard, etc.
├── security/
│   ├── signals.py              # Rule-based injection scorer
│   ├── simulator/diff_engine.py
│   ├── classifier/cvss_scorer.py
│   └── routing/policy_engine.py
├── analysis/parser/            # Solidity AST parser
├── tests_fasha-1/              # Phase 1 unit tests
├── tests_fasha2/               # Phase 2 integration test reports
├── tests_fasha-3/              # Phase 3 integration test reports
├── tests_fasha-4/              # Phase 4 E2E test reports
└── README.md

Deployment
Requirements

GenLayer Studio (browser) or GenLayer CLI
Python 3.8+

Deploy via GenLayer Studio

Open GenLayer Studio
Upload FulGenRoute.py
Click Deploy
Copy the contract address
Open frontend/config.js and paste the address

Deploy via CLI
bashgenlayer deploy FulGenRoute.py --network testnet
Usage example
python# Step 1 — classify
result = contract.route("Transfer 100 USDC to Alice")
# → {"executor": "financial_executor", "confidence": 95, "source": "fresh", "key": "intent_..."}

# Step 2 — persist
contract.commit_route(
    user_input="Transfer 100 USDC to Alice",
    executor="financial_executor",
    confidence=95,
    source="fresh",
    reason="Standard financial transfer"
)

# Step 3 — verify
contract.get_traces()
# → [{"input": "Transfer 100 USDC to Alice", "executor": "financial_executor", ...}]

Frontend
Open frontend/index.html in a browser. Enter the deployed contract address and RPC URL. The dashboard shows:

Risk Score Card — confidence, executor, source, and routing key for each request
Vulnerability Report — findings from analyze_contract pipeline
Routing Traces — full history of all routed requests
Security Reports — all analyze_contract results with risk scores


The frontend uses GenLayer's JSON-RPC API to call view methods (get_traces, get_all_reports) and displays results in real time. Write methods (route, commit_route) must still be called via GenLayer Studio or CLI.


Test Results
Phase 1 — Unit Tests (Python modules)
11 tests across 4 modules. Run from project root:
bashcd AI-Smart-Contract-Security-Execution-System
python -m pytest tests_fasha-1/ -v
ModuleTestsResultcvss_scorer.py3✅ Passsignals.py2✅ Passdiff_engine.py3✅ Passpolicy_engine.py3✅ Pass
Phase 2 — Contract Method Tests (GenLayer Studio)
32 manual tests across threshold, executor, outcome, security, and analysis blocks.
30/32 passed. 2 failures were prompt injection attacks that bypassed LLM-based detection (documented as known limitations).
Phase 3 — Integration Tests
8 tests verifying cross-method state persistence.
8/8 passed. Key finding: route() + commit_route() two-step pattern required for storage persistence.
Phase 4 — E2E Scenarios
5 full user scenarios including security audit flow, injection stress test, memory stress, boundary values, and feedback loop.
5/5 passed. All deviations were environment limitations, not contract bugs.
See /tests_fasha-1/, /tests_fasha2/, /tests_fasha-3/, /tests_fasha-4/ for full reports and transaction hashes.

Known Limitations (v1)
LimitationStatusNotesTwo-step routingArchitecture constraintGenLayer does not persist storage from nondet methods. route() + commit_route() is the required pattern.Russian/non-ASCII injectionsPartial mitigationINJECTION_PATTERNS covers English only. LLM catches many cases anyway (tested: Russian blocked in S-02).analyze_contract source limit8000 chars maxLarge contracts need to be split or summarized before analysis.Disagree on LLM methodsExpectedAll validators run independently with different LLMs — byte-identical output is impossible. FINALIZED = correct result.FulGenRoute schema errorUnresolvedFulGenRoute has additional fields that cause schema issues on some GenLayer builds. TestGenRoute (same logic, minimal schema) deploys reliably.

Implementation Status
ComponentStatusNotesIntent Router✅ CompleteLLM + rule-based pre-filterExecutor Layer✅ Complete4 built-in + dynamic registrationMemory Layer✅ CompleteCircular buffer (MAX 200 traces, 100 reports, 500 memory keys)Input Sanitizer✅ Complete20+ injection patterns + uncertainty detectionOwner access control✅ Completerecord_outcome, register_executor, set_threshold — owner-onlyStorage persistence✅ Complete via commit patternTwo-step route+commit solves GenLayer nondet constraintConsensus Fallback✅ CompleteThreshold-based fallback to consensus_executorFrontend Dashboard✅ CompleteView methods connected; write methods via Studio

Technical Foundation
GenRoute uses three GenLayer capabilities:

GenVM — executes LLM calls inside smart contract logic via run_nondet_unsafe
Optimistic Democracy — multi-validator consensus where each node runs the contract independently with a different LLM model
Intelligent Contracts — native Python contracts with AI decision logic


License
MIT License — Built for the GenLayer ecosystem.
