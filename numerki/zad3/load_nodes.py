def load_nodes(file, selected_function):
    """Pobiera z pliku węzły x i na podstawie przekazanej funkcji
    oblicza wartość w y"""
    x_nodes = []
    y_nodes = []
    with open(file, 'r') as f:
        for line in f:
            line_content = line.strip()
            if line_content:
                x_val = float(line_content)
                x_nodes.append(x_val)
                y_val = selected_function(x_val)
                y_nodes.append(y_val)
        return x_nodes, y_nodes
