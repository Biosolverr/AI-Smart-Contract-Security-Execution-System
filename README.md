[README.md](https://github.com/user-attachments/files/27248532/README.md)
# GenRoute AI

AI-powered intent routing meta-layer built on top of GenLayer.

## Overview

GenRoute is an intelligent routing middleware that sits between user input and blockchain execution. It analyzes natural language intents, classifies them using LLMs, routes them to appropriate executors, learns from historical outcomes, and triggers multi-validator consensus for ambiguous or high-risk operations.

Unlike traditional smart contracts with hardcoded logic paths, GenRoute dynamically determines execution routes based on semantic understanding of user requests.

## Core Functionality

### Intent Classification
The system parses free-form natural language input through an integrated LLM to determine the nature of the requested operation. Input sanitization mechanisms are applied before model invocation to mitigate prompt injection attacks.

### Executor Routing
Based on classification results, requests are routed to specialized executors:

| Executor | Purpose | Cost Tier |
|----------|---------|-----------|
| `financial_executor` | Payments, DeFi operations, token transfers | High |
| `audit_executor` | Smart contract security analysis, vulnerability scanning | Medium |
| `social_executor` | DAO governance, proposals, voting mechanisms | Low |
| `consensus_executor` | Ambiguous or high-risk operations requiring multi-validator approval | High |

New executors can be registered by contract owners through the `register_executor()` method.

### Adaptive Memory System
The routing layer maintains a history of executed intents and their outcomes. When an identical or similar intent is encountered, the system applies a confidence boost based on historical success rates. This creates a feedback loop where routing accuracy improves over time.

### Consensus Fallback Mechanism
When the LLM's confidence score falls below a configurable threshold (default: 70%), the request is automatically routed through the consensus executor. This ensures that uncertain classifications receive additional validation before execution.

## Architecture
User Intent (Natural Language)
↓
[Input Sanitizer]
↓
[LLM Intent Classifier] → Confidence Score
↓
┌────┴────┐
│ │
High Conf. Low Conf. (< threshold)
│ │
↓ ↓
[Executor [Consensus
Selection] Fallback]
│ │
└────┬────┘
↓
[Memory Update] ← Record outcome for learning
↓
[Execution on GenLayer]

text

## Repository Structure
genroute-ai/
├── GenRoute.py # Main intelligent contract implementation
├── contracts/ # Contract deployment artifacts
│ └── tests/ # Contract test suites
├── frontend/ # Dashboard and UI components
│ ├── dashboard/ # Monitoring interface
│ ├── app.js # Frontend application logic
│ └── index.html # Entry point
├── security/ # Security analysis modules
│ ├── attack_classifier.py # Attack pattern detection
│ ├── attacks/ # Known attack vectors
│ ├── classifier/ # Classification algorithms
│ ├── pipeline/ # Security processing pipeline
│ ├── routing/ # Secure routing logic
│ └── simulator/ # Attack simulation tools
├── analysis/ # Data analysis utilities
│ ├── graph/ # Graph-based analysis
│ └── parser/ # Input parsing modules
├── product/ # Product configuration and API
│ ├── api/ # API definitions
│ ├── config.py # Configuration settings
│ └── main.py # Application entry point
├── scripts/ # Deployment and utility scripts
│ ├── deploy.py # Deployment automation
│ └── run_full_pipeline.py # End-to-end pipeline execution
└── workspace/ # Development workspace

text

## Installation and Deployment

### Prerequisites
- GenLayer CLI or access to GenLayer Studio
- Python 3.x environment
- Network access to GenLayer testnet or mainnet

### Deployment Steps

1. **Deploy the contract:**
   ```bash
   # Using GenLayer CLI
   genlayer deploy GenRoute.py --network testnet
   
   # Or via GenLayer Studio - upload GenRoute.py and deploy
Route an intent:

python
contract.route("Vote for proposal #42")
# Returns: "social_executor"
Record execution outcomes:

python
contract.record_outcome("intent_a3f2c1d0", "social_executor", success=True)
# Updates memory for future confidence boosting
Configure consensus threshold:

python
contract.set_threshold(80)  # More conservative routing
contract.set_threshold(50)  # More permissive routing
Public API Reference
Method	Type	Description
route(user_input)	write	Classifies intent and returns target executor name
record_outcome(key, executor, success)	write	Updates routing memory with execution outcome
register_executor(name, description, tier, boost)	write	Registers new executor (owner-only)
set_threshold(value)	write	Sets consensus fallback threshold (owner-only)
get_threshold()	view	Returns current consensus threshold
get_executors()	view	Lists all registered executors
get_traces()	view	Returns routing history
get_failure_log()	view	Returns failure history
memory_size()	view	Returns count of entries in routing memory
Implementation Status
Component	Status	Notes
Intent Router	✓ Complete	LLM-based classification implemented
Executor Layer	✓ Complete	Four built-in executors operational
Memory Layer	✓ Complete	Outcome recording and confidence boosting functional
Input Sanitizer	✓ Complete	Basic prompt injection mitigation
Consensus Fallback	⚠ Partial	Currently a routing label; multi-model voting planned for v2
Memory Cap	⚠ Planned	Unbounded growth; LRU/circular buffer in v2
Executor Removal	⚠ Planned	Deregistration functionality in v2
Current State: Prototype stage, tested on GenLayer Testnet. Not recommended for production use without addressing known limitations.

Security Considerations
A comprehensive security audit is available in the codebase. Key identified risks:

Prompt Injection: While input sanitization is implemented, the system is not fully immune. LLM post-validation serves as secondary defense.

Unrestricted Memory Writes: The record_outcome() method accepts calls from any address, allowing potential memory poisoning. Access control mechanisms planned for v2.

Unbounded Storage Growth: Traces, memory entries, and failure logs have no capacity limits, which could lead to excessive gas costs or storage exhaustion. Mitigation via LRU eviction and circular buffers scheduled for v2.

Consensus Mechanism Limitation: The consensus_executor currently functions as a routing label rather than executing genuine multi-AI validation. True multi-model voting architecture is under development.

Risk Assessment: MEDIUM to HIGH for production deployments without v2 enhancements.

Technical Foundation
GenRoute leverages GenLayer's capabilities:

GenVM: Enables non-deterministic LLM execution within smart contracts

Optimistic Democracy: Multi-validator consensus for dispute resolution

Intelligent Contracts: Native support for AI-driven decision logic

The system is designed as a complement to GenLayer, not a replacement. It orchestrates how user intents are processed before being submitted to the underlying blockchain for execution.

Use Cases
DeFi Protocols: Automatic routing of complex financial transactions to appropriate validators

DAO Governance: Intelligent classification of proposals and voting operations

Security Auditing: Pre-execution vulnerability scanning for high-risk operations

Cross-Chain Bridges: Intent-based routing for multi-chain operations

NFT Marketplaces: Automated handling of minting, trading, and royalty distributions

Roadmap
v2 Planned Features:

Multi-model consensus voting implementation

Access control for memory operations

Storage cap enforcement with LRU eviction

Executor deregistration capability

Enhanced prompt injection detection

Reputation scoring for executors

License
MIT License - Developed for the GenLayer ecosystem.
