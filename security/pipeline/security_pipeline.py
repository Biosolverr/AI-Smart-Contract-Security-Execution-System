from analysis.parser.solidity_ast_parser import SolidityASTParser
from analysis.parser.call_graph_builder import CallGraphBuilder
from analysis.parser.storage_mapping import StorageMapping
from analysis.parser.vulnerability_binding import VulnerabilityBinding
from analysis.grapf.graph_engine import GraphEngine
from security.attask.exploit_targeting_engine import ExploitTargetingEngine


class SecurityPipeline:

    def run(self, user_input: str, contract_code: str = None):
        source = contract_code or ""

        # 1. AST parsing with warnings
        ast = SolidityASTParser().parse(source)
        ast_warnings = ast.get("warnings", [])

        # 2. Call graph (real edges only)
        call_graph = CallGraphBuilder().build(ast)

        # 3. Storage mapping (uses state_vars from AST)
        storage = StorageMapping().map(ast)

        # 4. Vulnerability binding (uses AST properties)
        bindings = VulnerabilityBinding().bind(ast)

        # 5. Graph build
        graph = GraphEngine().build(call_graph, storage, bindings)

        # 6. Exploit targeting (sorted by CVSS)
        exploits = ExploitTargetingEngine().target(bindings)

        return {
            "ast": ast,
            "graph": graph,
            "exploits": exploits,
            "bindings": bindings,
            "ast_warnings": ast_warnings
        }
