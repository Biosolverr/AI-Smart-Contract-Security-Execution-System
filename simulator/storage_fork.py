class StorageFork:

    def fork(self, state: dict):

        return {
            "balances": state.get("balances", {}).copy(),
            "storage": state.get("storage", {}).copy()
        }
