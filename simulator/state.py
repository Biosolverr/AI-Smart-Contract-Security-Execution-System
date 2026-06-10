from dataclasses import dataclass, field

@dataclass
class ContractState:
    balances: dict = field(default_factory=dict)
    storage: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)
