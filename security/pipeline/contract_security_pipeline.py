from analysis.parser.solidity_ast_parser import SolidityASTParser
from analysis.parser.call_graph_builder import CallGraphBuilder
from analysis.parser.storage_mapping import StorageMapping
from analysis.parser.vulnerability_binding import VulnerabilityBinding
from analysis.graph.graph_engine import GraphEngine
from security.attacks.exploit_targeting_engine import ExploitTargetingEngine

class ContractSecurityPipeline:

    def run(self, solidity_code: str):

        # 1. AST
        ast = SolidityASTParser().parse(solidity_code)

        # 2. CALL GRAPH
        call_graph = CallGraphBuilder().build(ast)

        # 3. STORAGE MAP
        storage = StorageMapping().map(ast)

        # 4. VULNERABILITY BINDING
        bindings = VulnerabilityBinding().bind(ast)

        # 5. GRAPH BUILD
        graph = GraphEngine().build(call_graph, storage, bindings)

        # 6. EXPLOIT TARGETING
        exploits = ExploitTargetingEngine().target(bindings)

        return {
            "ast": ast,
            "graph": graph,
            "bindings": bindings,
            "exploits": exploits
        }
