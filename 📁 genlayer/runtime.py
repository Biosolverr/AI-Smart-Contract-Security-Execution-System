from genlayer.adapter import GenLayerAdapter


adapter = GenLayerAdapter()


def handle_request(context: dict):
    """
    This mimics GenLayer runtime call
    """

    return adapter.route(context)
