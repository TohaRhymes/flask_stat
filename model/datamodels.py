from dataclasses import dataclass
import re


@dataclass
class Constant:
    constant_name: str
    constant_value: float