from security.pipeline.security_pipeline import SecurityPipeline
from security.simulator.execution_simulator import ExecutionSimulator


contract = """
function withdraw() onlyOwner {}
function mint() {}
function transfer() {}
"""

# =========================
# 🧠 PIPELINE (CONTRACT UNDERSTANDING)
# =========================
pipeline = SecurityPipeline()
analysis = pipeline.run("withdraw exploit", contract)

# =========================
# 🧪 SIMULATOR (ATTACK EXECUTION)
# =========================
simulator = ExecutionSimulator()

result = simulator.simulate(
    attack_input="withdraw exploit",
    analysis=analysis
)

# =========================
# 📊 OUTPUT
# =========================
print("=== ANALYSIS ===")
print(analysis)

print("\n=== EXECUTION RESULT ===")
print(result)
