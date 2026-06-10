from security.pipeline.security_pipeline import SecurityPipeline
from security.simulator.execution_simulator import ExecutionSimulator
from security.classifier.cvss_scorer import CVSSScorer


class SecurityPlugin:
    """
    Main entrypoint for the GenLayer adapter.
    Orchestrates analysis pipeline → simulation → scoring → routing decision.
    """

    def __init__(self):
        self.pipeline = SecurityPipeline()
        self.simulator = ExecutionSimulator()
        self.scorer = CVSSScorer()

    def execute(self, context: dict) -> dict:
        contract = context.get("contract", "")
        input_data = context.get("input", "")

        # 1. Static analysis
        analysis = self.pipeline.run(input_data, contract)

        # 2. Attack simulation
        result = self.simulator.simulate(
            attack_input=input_data,
            analysis=analysis
        )

        # 3. CVSS scoring (replaces the broken `len(edges) * 10`)
        cvss_result = self.scorer.score_targets(analysis.get("exploits", []))
        risk_score = cvss_result["overall_cvss"]

        # 4. Route decision: highest-severity exploit drives executor selection
        exploits = analysis.get("exploits", [])
        if exploits:
            top = exploits[0]  # Already sorted by CVSS descending
            executor = top["function"]
        else:
            executor = "default_executor"

        return {
            "executor": executor,
            "risk_score": risk_score,
            "overall_severity": cvss_result["overall_severity"],
            "state": result["state"],
            "logs": result["logs"],
            "graph": analysis["graph"],
            "cvss_details": cvss_result["details"],
            "ast_warnings": analysis.get("ast_warnings", [])
        }
