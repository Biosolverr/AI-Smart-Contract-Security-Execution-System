from security.attacks.exploit_targeting_engine import ExploitTargetingEngine


class CVSSScorer:
    """
    Scores a list of exploit targets using CVSS 3.1 base scores.
    Returns aggregate risk score (max severity wins) plus per-finding detail.
    """

    _ENGINE = ExploitTargetingEngine()

    def score(self, exploit_type: str) -> dict:
        """Score a single vulnerability type."""
        info = self._ENGINE.EXPLOIT_MAP.get(exploit_type)
        if info:
            return {"cvss": info["cvss"], "severity": info["severity"]}
        return {"cvss": 5.0, "severity": "MEDIUM"}

    def score_targets(self, targets: list) -> dict:
        """
        Score a list of targets (output of ExploitTargetingEngine.target()).
        Returns overall max CVSS, overall severity label, and per-target detail.
        """
        if not targets:
            return {"overall_cvss": 0.0, "overall_severity": "NONE", "details": []}

        details = [
            {
                "function": t["function"],
                "vulnerability": t["vulnerability"],
                "cvss": t.get("cvss", 5.0),
                "severity": t.get("severity", "MEDIUM")
            }
            for t in targets
        ]

        max_cvss = max(d["cvss"] for d in details)
        overall_severity = self._severity_label(max_cvss)

        return {
            "overall_cvss": max_cvss,
            "overall_severity": overall_severity,
            "details": details
        }

    @staticmethod
    def _severity_label(score: float) -> str:
        if score >= 9.0:
            return "CRITICAL"
        if score >= 7.0:
            return "HIGH"
        if score >= 4.0:
            return "MEDIUM"
        return "LOW"
