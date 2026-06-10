class StorageMapping:
    """
    Maps contract functions to the state variables they likely read/write,
    based on AST data extracted by SolidityASTParser.
    """

    # Known state-variable-like patterns per vulnerability type
    WRITE_HINTS = {
        "withdraw": ["balances", "vault", "totalSupply"],
        "mint":     ["supply", "balances", "totalSupply"],
        "burn":     ["supply", "balances", "totalSupply"],
        "transfer": ["balances", "allowances"],
        "approve":  ["allowances"],
        "set":      ["config", "owner", "settings"],
        "init":     ["owner", "initialized"],
    }

    def map(self, ast: dict) -> dict:
        functions = ast.get("functions", [])
        state_var_names = [v["name"] for v in ast.get("state_vars", [])]
        storage = {}

        for fn in functions:
            name = fn["name"]
            raw = fn.get("raw", "").lower()
            accessed = []

            # Check declared state vars referenced in function body
            for var in state_var_names:
                if var.lower() in raw:
                    accessed.append(var)

            # Apply keyword hints for common patterns
            name_lower = name.lower()
            for keyword, vars_list in self.WRITE_HINTS.items():
                if keyword in name_lower:
                    for v in vars_list:
                        if v not in accessed:
                            accessed.append(v)

            storage[name] = accessed if accessed else ["no_known_state"]

        return storage
