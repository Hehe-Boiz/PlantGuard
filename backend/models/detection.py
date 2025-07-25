from dataclasses import dataclass
from typing import Tuple

@dataclass
class Detection:
    cls_id: int
    conf: float
    box: Tuple[int, int, int, int]