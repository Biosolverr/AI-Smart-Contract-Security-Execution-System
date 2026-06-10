class DiffEngine:
    """
    Computes state diff between two contract snapshots.
    Safe against missing keys — uses .get() with defaults.
    """

    def compare(self, before: dict, after: dict) -> dict:
        """
        Compare two state dicts. Returns a dict of changed keys with
        {"before": ..., "after": ...} values. Returns {} if no changes.
        """
        changes = {}

        all_keys = set(before) | set(after)
        for k in all_keys:
            b = before.get(k)
            a = after.get(k)
            if b != a:
                if isinstance(b, dict) and isinstance(a, dict):
                    nested = self.compare(b, a)
                    if nested:
                        changes[k] = nested
                else:
                    changes[k] = {"before": b, "after": a}

        return changes

    def diff(self, before: dict, after: dict) -> list:
        """Legacy list-format diff (kept for backward compat)."""
        changes = []

        before_balances = before.get("balances", {})
        after_balances = after.get("balances", {})
        for k in set(before_balances) | set(after_balances):
            b = before_balances.get(k, 0)
            a = after_balances.get(k, 0)
            if b != a:
                changes.append(f"balance[{k}]: {b} → {a} (delta {a - b:+})")

        before_storage = before.get("storage", {})
        after_storage = after.get("storage", {})
        for k in set(before_storage) | set(after_storage):
            b = before_storage.get(k)
            a = after_storage.get(k)
            if b != a:
                changes.append(f"storage[{k}]: {b!r} → {a!r}")

        scalar_keys = set(before) | set(after)
        scalar_keys -= {"balances", "storage"}
        for k in scalar_keys:
            b = before.get(k)
            a = after.get(k)
            if b != a:
                changes.append(f"{k}: {b!r} → {a!r}")

        return changes
