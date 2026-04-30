import genlayer as gl
import json


def _llm_attack_leader(prompt: str) -> str:
    raw = gl.nondet.exec_prompt(prompt).strip()
    if raw.startswith("```"):
        raw = "\n".join(
            l for l in raw.splitlines()
            if not l.strip().startswith("```")
        ).strip()
    try:
        parsed = json.loads(raw)
        return raw if isinstance(parsed, list) else "[]"
    except Exception:
        return "[]"


def _llm_attack_validator(res: str) -> bool:
    if not isinstance(res, str):
        return False
    try:
        d = json.loads(res)
        return (
            isinstance(d, list)
            and all(
                isinstance(step, str) and len(step) > 0
                for step in d
            )
        )
    except Exception:
        return False


class LLMAttackGenerator:
    """
    Generates attack step sequences via GenLayer nondet consensus.
    Falls back to deterministic templates on validation failure.
    """

    FALLBACKS = {
        "reentrancy": [
            "step1: call withdraw() from attacker contract",
            "step2: attacker fallback() re-enters withdraw() before balance update",
            "step3: repeat recursively until vault drained",
            "step4: state update finally runs with zero balance"
        ],
        "auth": [
            "step1: identify privileged function with missing onlyOwner modifier",
            "step2: call directly from attacker address",
            "step3: privilege escalated — owner state overwritten"
        ],
        "drain": [
            "step1: call transfer() with amount exceeding balance check",
            "step2: missing require() allows underflow",
            "step3: attacker receives excess funds"
        ]
    }

    def generate(self, intent: str) -> list:
        intent_lower = intent.lower()

        prompt = (
            "You are a smart contract exploit researcher.\n"
            f"Generate a step-by-step attack chain for intent: '{intent}'\n\n"
            "Rules:\n"
            "- Return ONLY a JSON array of strings\n"
            "- Each string is one attack step (e.g. 'step1: call withdraw()')\n"
            "- 3 to 6 steps maximum\n"
            "- No markdown, no explanation, no preamble\n\n"
            'Example: ["step1: identify target", "step2: craft payload", "step3: execute"]'
        )

        try:
            raw = gl.vm.run_nondet_unsafe(
                lambda p=prompt: _llm_attack_leader(p),
                lambda res: _llm_attack_validator(res)
            )
            steps = json.loads(raw) if isinstance(raw, str) else []
            if steps:
                return steps
        except Exception:
            pass

        # Fallback to deterministic templates
        for key, steps in self.FALLBACKS.items():
            if key in intent_lower:
                return steps

        return ["step1: analyze target contract", "step2: identify entry point", "step3: execute exploit"]
