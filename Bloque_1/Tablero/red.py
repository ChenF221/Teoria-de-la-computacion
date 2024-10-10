import matplotlib.pyplot as plt
import networkx as nx

def dibujar_grafo_desde_archivo(archivo, mensaje):

    G = nx.DiGraph()

    with open(archivo, 'r') as f:
        rutas = [line.strip().split(',') for line in f]
        longitud_ruta = len(rutas[0])

        
        posiciones = {}
        for idx, ruta in enumerate(rutas):
            for pos, estado in enumerate(ruta):
                nodo = (pos + 1, int(estado))
                if nodo not in posiciones:
                    posiciones[nodo] = (pos, -idx)
                if pos < longitud_ruta - 1:
                    nodo_siguiente = (pos + 2, int(ruta[pos + 1]))
                    G.add_edge(nodo, nodo_siguiente)

    
    plt.figure(figsize=(9, 8))
    num_columnas = longitud_ruta
    distancia_entre_columnas = 2  
    
    for columna in range(1, num_columnas + 1):
        nodos_en_columna = [nodo for nodo in posiciones.keys() if nodo[0] == columna]
        
        for idx, nodo in enumerate(nodos_en_columna):
            posiciones[nodo] = (columna, -idx * distancia_entre_columnas)
    
    nx.draw(G, pos=posiciones, with_labels=False, node_size=800, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    etiquetas = {nodo: f"{nodo[1]}" for nodo in G.nodes()}
    nx.draw_networkx_labels(G, pos=posiciones, labels=etiquetas, font_color='black', font_size=8)
    
   
    plt.text(0.5, 0.95, mensaje, ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
    
    plt.title('Graph of Node Connections Across Positions')
    plt.axis('off')
    plt.show()


dibujar_grafo_desde_archivo('Bloque_1\\Tablero\\all_routes_player1.txt', "Red del jugador 1")
dibujar_grafo_desde_archivo('Bloque_1\\Tablero\\all_routes_player2.txt', "Red del jugador 2")