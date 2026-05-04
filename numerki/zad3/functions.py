import math
from typing import Callable, TypedDict
from horner import *

class FunctionData(TypedDict):
    opis: str
    f: Callable[[float], float]

FUNCTIONS: dict[str, FunctionData] = {
    "1": {
        "opis": "Wielomian: x^4 - x^2 + 3x - 2",
        "f": lambda x: horner(x, [1.0, 0.0, -1.0, 3.0, -2.0], 5)
    },
    "2": {
        "opis": "Trygonometryczna: 2cos(0.5x) + 1",
        "f": lambda x: 2 * math.cos(0.5 * x) + 1
    },
    "3": {
        "opis": "Wykładnicza: e^x - 2",
        "f": lambda x: math.exp(x) - 2
    },
    "4": {
        "opis": "Złożona: sin(x^2) + 3x - 3",
        "f": lambda x: math.sin(x * x) + 3 * x - 3
    },
    "5": {
        "opis": "Wartość bezwzględna: |x|",
        "f": lambda x: math.fabs(x)
    }
}