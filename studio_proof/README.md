# GenLayer Studio Proof

This folder contains on-chain execution evidence from GenLayer Studio (Testnet Bradbury).

## Files

- `deployment.json` — contract deploy transaction
- `route_proof.json` — `route()` + `commit_route()` execution
- `analyze_proof.json` — `analyze_contract()` execution
- `get_traces_proof.json` — `get_traces()` view call showing stored routing history

## How to reproduce

1. Open https://studio.genlayer.com
2. Load `FulGenRoute.py`
3. Deploy → copy contract address
4. Run methods in order as shown in each JSON file
