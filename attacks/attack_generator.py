from .exploit_templates import TEMPLATES

class AttackGenerator:

    def generate(self, intent: str):

        if "reentrancy" in intent:
            return TEMPLATES["reentrancy"]

        if "auth" in intent:
            return TEMPLATES["auth_bypass"]

        return "generic_attack"
