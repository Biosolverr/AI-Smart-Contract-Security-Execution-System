from fastapi import FastAPI
from security.pipeline.security_pipeline import SecurityPipeline
from security.simulator.execution_simulator import ExecutionSimulator

app = FastAPI()

pipeline = SecurityPipeline()
simulator = ExecutionSimulator()


@app.post("/analyze")
def analyze(payload: dict):

    contract = payload.get("contract", "")
    input_data = payload.get("input", "")

    analysis = pipeline.run(input_data, contract)

    return {
        "analysis": analysis
    }


@app.post("/simulate")
def simulate(payload: dict):

    input_data = payload.get("input", "")
    analysis = payload.get("analysis", None)

    result = simulator.simulate(input_data, analysis)

    return result


@app.post("/full")
def full_pipeline(payload: dict):

    contract = payload.get("contract", "")
    input_data = payload.get("input", "")

    analysis = pipeline.run(input_data, contract)

    result = simulator.simulate(input_data, analysis)

    return {
        "analysis": analysis,
        "result": result
    }
