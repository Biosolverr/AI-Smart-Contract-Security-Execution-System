from .signals import rule_based_score
import genlayer as gl


def llm_score(user_input: str) -> int:
    def leader():
        result = gl.nondet.exec_prompt(f"""
You are a security classifier.

Return ONLY a number 0-100:
0 = safe
100 = attack

Input:
{user_input}
""")
        return result.strip()

    def validator(res):
        try:
            val = int(res)
            return 0 <= val <= 100
        except:
            return False

    out = gl.vm.run_nondet_unsafe(leader, validator)

    try:
        return int(out)
    except:
        return 50


def attack_score(user_input: str):
    rule_score = rule_based_score(user_input)
    llm_s = llm_score(user_input)

    final_score = int(rule_score * 0.6 + llm_s * 0.4)

    if final_score < 30:
        label = "safe"
        action = "allow"
    elif final_score < 70:
        label = "suspicious"
        action = "review"
    else:
        label = "attack"
        action = "block"

    return {
        "label": label,
        "severity": final_score,
        "action": action,
        "rule_score": rule_score,
        "llm_score": llm_s
    }
