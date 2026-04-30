class ExecutionSimulator:

    def simulate(self, attack_input: str, analysis: dict = None):

        # =========================
        # 🧱 INITIAL STATE
        # =========================
        state = {
            "vault": 5000,
            "attacker": 100,
            "owner": "admin"
        }

        logs = []

        # =========================
        # 🎯 TARGET FROM ANALYSIS
        # =========================
        target_function = None

        if analysis and "exploits" in analysis:
            exploits = analysis["exploits"]

            if exploits and len(exploits) > 0:
                target_function = exploits[0].get("function")

        # =========================
        # ⚔️ ATTACK EXECUTION LOGIC
        # =========================

        if "withdraw" in attack_input or target_function == "withdraw":

            logs.append("withdraw exploited")

            state["vault"] -= 1000
            state["attacker"] += 1000

        if "mint" in attack_input:

            logs.append("mint triggered")

            state["attacker"] += 500

        if "reentrancy" in attack_input:

            logs.append("reentrancy exploit executed")

            state["vault"] -= 2000
            state["attacker"] += 2000

        if "owner" in attack_input:

            logs.append("owner override")

            state["owner"] = "attacker"

        # =========================
        # 📦 RESULT
        # =========================
        return {
            "state": state,
            "logs": logs,
            "target_function": target_function,
            "analysis_used": analysis is not None
        }
