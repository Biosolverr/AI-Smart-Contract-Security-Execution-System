class DiffEngine:
    """
    Computes state diff between two contract snapshots.
    Safe against missing keys — uses .get() with defaults.
    """

    def diff(self, before: dict, after: dict) -> list:
        changes = []

        before_balances = before.get("balances", {})
        after_balances = after.get("balances", {})
        all_balance_keys = set(before_balances) | set(after_balances)
        for k in all_balance_keys:
            b = before_balances.get(k, 0)
            a = after_balances.get(k, 0)
            if b != a:
                changes.append(f"balance[{k}]: {b} → {a} (delta {a - b:+})")

        before_storage = before.get("storage", {})
        after_storage = after.get("storage", {})
        all_storage_keys = set(before_storage) | set(after_storage)
        for k in all_storage_keys:
            b = before_storage.get(k)
            a = after_storage.get(k)
            if b != a:
                changes.append(f"storage[{k}]: {b!r} → {a!r}")

        # Top-level scalar fields (vault, owner, etc.)
        scalar_keys = set(before) | set(after)
        scalar_keys -= {"balances", "storage"}
        for k in scalar_keys:
            b = before.get(k)
            a = after.get(k)
            if b != a:
                changes.append(f"{k}: {b!r} → {a!r}")

        return changes
