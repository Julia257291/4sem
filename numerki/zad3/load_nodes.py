from typing import Callable


def load_nodes(file_path: str, function: Callable[[float], float]) -> tuple[list[float], list[float]]:
    x_nodes: list[float] = []
    y_nodes: list[float] = []

    with open(file_path, 'r') as f:
        for line in f:
            parts: list[str] = line.split()
            for part in parts:
                x_val: float = float(part)
                x_nodes.append(x_val)

    x_nodes.sort()

    for node in x_nodes:
        y: float = function(node)
        y_nodes.append(y)

    return x_nodes, y_nodes
