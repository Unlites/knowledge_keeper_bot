from dataclasses import dataclass
from typing import Any


@dataclass
class UsecaseResult:
    data: Any = None
    success: bool = True