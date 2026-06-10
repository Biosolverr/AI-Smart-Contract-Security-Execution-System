# GenRoute — AI Smart Contract Security Pipeline

AI-powered middleware built natively on GenLayer. Classifies natural language user intent,
routes it to the correct executor, and runs a full 4-layer security audit on Solidity smart
contracts — all inside an Intelligent Contract on Testnet Bradbury.

Live demo: https://ai-smart-contract-security-executio.vercel.app/
GitHub: https://github.com/Biosolverr/AI-Smart-Contract-Security-Execution-System

---

## What it does

- **Intent Router** — LLM classifies user input → routes to `financial`, `audit`, `social`, or `consensus` executor
- **Pre-filter** — 20+ rule-based injection patterns block attacks before the LLM is ever called
- **Security Pipeline** — parse → attack generation → simulation → CVSS scoring, fully on-chain
- **Routing Memory** — circular buffer caches results, system gets smarter over time
- **Dashboard UI** — deployed frontend shows risk scores, vulnerability reports, and full routing history

Uses `run_nondet_unsafe` for LLM calls, Optimistic Democracy for multi-validator consensus,
and a two-step `route() + commit_route()` pattern to solve GenLayer's nondet storage constraint.

---

## Quick Start

```bash
git clone https://github.com/Biosolverr/AI-Smart-Contract-Security-Execution-System
cd AI-Smart-Contract-Security-Execution-System
pip install -e .
python -m pytest tests/ -v
```

Expected output: **29 passed**.

---

## Repository Structure

```
FulGenRoute.py                  # Main Intelligent Contract (deploy to GenLayer)
setup.py                        # Package install
requirements.txt                # Test dependencies

analysis/
  parser/
    solidity_ast_parser.py      # Regex-based Solidity AST parser (functions, state vars, calls)
    call_graph_builder.py       # Intra- and inter-contract call graph
    storage_mapping.py          # Function → state variable access map
    vulnerability_binding.py    # Function → vulnerability type binding
  graph/
    graph_engine.py             # Build node/edge graph from pipeline outputs

security/
  classifier/
    cvss_scorer.py              # CVSS 3.1 base score calculator
    signals.py                  # Rule-based signal scoring (strings and vuln dicts)
  simulator/
    diff_engine.py              # Before/after state diff engine
    execution_simulator.py      # Attack execution simulation
    replay_system.py            # State replay
    state.py                    # State snapshot model
    storage_fork.py             # Storage fork for simulation isolation
    trace_recorder.py           # Execution trace recorder
  routing/
    policy_engine.py            # Risk-based routing policy decisions
    security_router.py          # Router with security gate
    security_gatekeeper.py      # Gatekeeper pre-check
    contract_function_router.py # Contract function-level routing
    function_policy_engine.py   # Per-function policy
  attacks/
    exploit_targeting_engine.py # CVSS-ranked exploit target generator
    attack_generator.py         # Template-based attack generator
    attack_chain_builder.py     # Multi-step attack chain builder
    llm_attack_generator.py     # LLM-powered attack generation
    exploit_templates.py        # Exploit template library
    auth_bypass.py              # Auth bypass exploits
    drain_attacks.py            # Fund drain exploits
    reentrancy.py               # Reentrancy exploits
  pipeline/
    security_pipeline.py        # Full 4-layer pipeline (parse→attacks→sim→classify)
    contract_security_pipeline.py # Alias pipeline
  attack_classifier.py          # Combined rule + LLM attack classifier
  routing_policy.py             # Score → routing mode policy
  signals.py                    # Re-export shim (backward compat)

tests/
  test_cvss_scorer.py           # CVSS score calculation (3 tests)
  test_diff_engine.py           # State diff engine (5 tests)
  test_policy_engine.py         # Routing policy engine (5 tests)
  test_security_pipeline.py     # Full pipeline integration (5 tests)
  test_signals.py               # Signal scoring (5 tests)
  test_solidity_parser.py       # Solidity AST parser incl. reentrancy detection (6 tests)

frontend/
  index.html                    # Dashboard UI (static, deployed on Vercel)
```

---

## Run Tests

```bash
python -m pytest tests/ -v
```

All 29 tests pass. Coverage:

| File | Tests |
|---|---|
| `security/classifier/cvss_scorer.py` | min / mid / max CVSS score |
| `security/simulator/diff_engine.py` | empty, simple change, nested, no change, added key |
| `security/routing/policy_engine.py` | allow, block (high risk), block (high value), warn, edge zero |
| `security/pipeline/security_pipeline.py` | runs, ast, exploits, graph, empty contract |
| `security/classifier/signals.py` | vuln dict low/high/critical, string injection, string clean |
| `analysis/parser/solidity_ast_parser.py` | simple, complex, functions, name, empty, reentrancy detection |

---

## Contract Architecture

`FulGenRoute.py` is a single GenLayer Intelligent Contract with two public write methods per feature:

### Intent Routing
- `route(user_input)` — classify intent via LLM, returns JSON routing decision (no storage write)
- `commit_route(...)` — persist routing result; only owner can call

### Contract Security Audit
- `analyze_contract(source, label)` — run full 4-layer security pipeline, returns JSON report
- `commit_analyze(...)` — persist audit result; only owner can call

### Read-only Views
- `get_report(index)` — single audit report by index
- `get_all_reports()` — all reports summary list
- `get_traces()` — full routing history
- `get_executors()` — registered executor list
- `get_route_key(user_input)` — routing memory key for a given input
- `get_threshold()` — current consensus threshold

### Admin
- `register_executor(name, description, cost_tier, confidence_boost)` — add executor
- `set_threshold(threshold)` — set consensus confidence threshold
- `record_outcome(key, executor, success)` — feedback loop for routing memory

---

## Notes on GenLayer Constraints

GenLayer does not allow writing to storage inside `run_nondet_unsafe`. This contract
uses a two-step pattern to work around this:

1. `route()` / `analyze_contract()` — call LLM via `run_nondet_unsafe`, return result as JSON string
2. `commit_route()` / `commit_analyze()` — receive the result values and persist them to storage

The frontend calls both steps and passes the Output values from step 1 directly to step 2.
