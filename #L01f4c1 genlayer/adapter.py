from genlayer.plugins.security_plugin import SecurityPlugin


class GenLayerAdapter:

    def __init__(self):
        self.plugin = SecurityPlugin()

    # =========================
    # 🔗 GENLAYER CALL
    # =========================
    def route(self, payload: dict):

        return self.plugin.execute(payload)
