from dataclasses import dataclass
from typing import Any
from enum import Enum


class UsecaseStatus(Enum):
    SUCCESS = 1
    UNAUTHORIZED = 2
    FAILURE = 3


@dataclass
class UsecaseResult:
    data: Any = None
    status: UsecaseStatus = UsecaseStatus.SUCCESS
