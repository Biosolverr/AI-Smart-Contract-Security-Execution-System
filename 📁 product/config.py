import os

class Config:

    ENV = os.getenv("ENV", "dev")

    ENABLE_SIMULATION = True
    ENABLE_GRAPH = True
    ENABLE_ATTACK_ENGINE = True

    ROUTING_THRESHOLD = 70
