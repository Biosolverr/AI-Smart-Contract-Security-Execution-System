class AttackChainBuilder:

    def build(self, steps: list):

        chain = []
        for i, step in enumerate(steps):
            chain.append({
                "step": i + 1,
                "action": step
            })

        return {
            "chain": chain,
            "length": len(chain)
        }
