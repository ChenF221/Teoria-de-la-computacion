import networkx as nx
import matplotlib.pyplot as plt

# Definir la tabla de transición como un diccionario
transiciones = {
    'A': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'A'},
    'B': {'w': 'B', 'e': 'D', 'b': 'A', 'a': 'A', 'y': 'A'},
    'C': {'w': 'B', 'e': 'C', 'b': 'E', 'a': 'A', 'y': 'A'},
    'D': {'w': 'B', 'e': 'C', 'b': 'F', 'a': 'A', 'y': 'A'},
    'E': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'G', 'y': 'A'},
    'F': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'G', 'y': 'A'},
    'G': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'H'},
    'H': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'A'},
}

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos
for nodo in transiciones:
    G.add_node(nodo)


# Agregar las transiciones como aristas y combinar etiquetas
edge_labels_dict = {}  # Diccionario para agrupar etiquetas por aristas
for nodo_actual, transiciones_letras in transiciones.items():
    for letra, nodo_destino in transiciones_letras.items():
        edge = (nodo_actual, nodo_destino)
        if edge not in edge_labels_dict:
            edge_labels_dict[edge] = []
        edge_labels_dict[edge].append(letra)

# Añadir las aristas al grafo con las etiquetas agrupadas
for (nodo_origen, nodo_destino), letras in edge_labels_dict.items():
    G.add_edge(nodo_origen, nodo_destino, label=",".join(letras))

# Colores para los nodos: los nodos 'F' y 'H' tendrán un color diferente
node_colors = ['lightblue' if nodo not in ['F', 'H'] else 'lightgreen' for nodo in G.nodes()]

# Dibujar el grafo
pos = nx.spring_layout(G, seed=42)  # Posiciones para los nodos
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=12, font_weight="bold", arrows=True)

# Etiquetas para las aristas
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


# Mostrar el grafo
plt.title("Grafo de Transiciones")
plt.show()