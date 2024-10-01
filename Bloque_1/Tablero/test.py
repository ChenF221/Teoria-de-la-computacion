import networkx as nx
import matplotlib.pyplot as plt

# 1. Crear un grafo dirigido
G = nx.DiGraph()

# 2. Añadir nodos y aristas
G.add_edges_from([(1, 2), (1, 4), (2, 1)])
#G.add_edges_from([(2, 1), (2, 3), (2, 5), (4, 5), (4, 7)])

# 3. Fijar la posición del nodo 1 y generar posiciones para los demás nodos
fixed_pos = {1: (-1, 0)}  # Fijar el nodo 1 en el lado izquierdo
pos = nx.spring_layout(G, pos=fixed_pos, fixed=[1], seed=42)

# 4. Dibujar el grafo con flechas
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=12)

# 5. Dibujar las aristas con flechas
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

# Mostrar el grafo
plt.show()
