class GraphEngine:

    def build(self, call_graph, storage_map, bindings):

        nodes = []
        edges = []

        for f, stores in storage_map.items():
            nodes.append({"id": f, "type": "function"})

            for s in stores:
                nodes.append({"id": s, "type": "storage"})
                edges.append({
                    "from": f,
                    "to": s,
                    "type": "writes_to"
                })

        for b in bindings:
            edges.append({
                "from": b,
                "to": bindings[b],
                "type": "vulnerability"
            })

        edges.extend(call_graph)

        return {
            "nodes": nodes,
            "edges": edges
        }
