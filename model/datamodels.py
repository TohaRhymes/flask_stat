from dataclasses import dataclass


@dataclass
class Constant:
    constant_name: str
    constant_value: float