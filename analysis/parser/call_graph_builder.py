import re


class CallGraphBuilder:
    """
    Builds a call graph from a parsed AST.
    Detects intra-contract function calls and external calls.
    """

    def build(self, ast: dict) -> list:
        functions = ast.get("functions", [])
        fn_names = {f["name"] for f in functions}
        graph = []

        for fn in functions:
            caller = fn["name"]
            body_text = fn.get("raw", "")

            # Intra-contract calls: find known function names called in body
            for callee in fn_names:
                if callee == caller:
                    continue
                # Match callee( but not inside comments or strings
                pattern = rf'\b{re.escape(callee)}\s*\('
                if re.search(pattern, body_text):
                    graph.append({
                        "from": caller,
                        "to": callee,
                        "type": "internal_call"
                    })

            # External calls already extracted by parser
            for ext in fn.get("external_calls", []):
                graph.append({
                    "from": caller,
                    "to": f"{ext['target']}.{ext['method']}",
                    "type": "external_call"
                })

        return graph
