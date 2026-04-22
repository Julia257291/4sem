def load_nodes(file, function):
    """Pobiera z pliku węzły x i na podstawie przekazanej funkcji
    oblicza wartość w y"""
    x_nodes = []
    y_nodes = []
    with open(file, 'r') as f:
        for line in f:
            parts = line.split()
            for part in parts:
                x_val = float(part)
                x_nodes.append(x_val)
    x_nodes.sort()
    for node in x_nodes:
        y = function(node)
        y_nodes.append(y)
    return x_nodes, y_nodes
