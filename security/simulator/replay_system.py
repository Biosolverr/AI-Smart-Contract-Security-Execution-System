class ReplaySystem:

    def replay(self, traces):

        timeline = []

        state = {"vault": 5000, "attacker": 100}

        for t in traces:

            if "drain" in t["attack"]:
                state["vault"] -= 1000
                state["attacker"] += 1000

            timeline.append({
                "step": t["attack"],
                "state": state.copy()
            })

        return {
            "timeline": timeline,
            "final_state": state
        }
