import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
import networkx as nx


# 3x3
# boardstate = {
#     1: {'r': [2, 4], 'b': [5]},
#     2: {'r': [4, 6], 'b': [1, 3, 5]},
#     3: {'r': [2, 6], 'b': [5]},
#     4: {'r': [2, 8], 'b': [1, 5, 7]},
#     5: {'r': [2, 4, 6, 8], 'b': [1, 3, 7, 9]},
#     6: {'r': [2, 8], 'b': [3, 5, 9]},
#     7: {'r': [4, 8], 'b': [5]},
#     8: {'r': [4, 6], 'b': [5, 7, 9]},
#     9: {'r': [6, 8], 'b': [5]}
# }


# 5x5
boardstate = {
    1:  {'r': [2, 6], 'b': [7]},
    2:  {'r': [6, 8], 'b': [1, 3, 7]},
    3:  {'r': [2, 8, 4], 'b': [7, 9]},
    4:  {'r': [8, 10], 'b': [3, 5, 9]},
    5:  {'r': [4, 10], 'b': [9]},
    
    6:  {'r': [2, 12], 'b': [1, 7, 11]},
    7:  {'r': [2, 6, 8, 12], 'b': [1, 3, 11, 13]},
    8:  {'r': [2, 4, 12, 14], 'b': [3, 7, 9, 13]},
    9:  {'r': [4, 8, 10, 14], 'b': [3, 5, 13, 15]},
    10: {'r': [4, 14], 'b': [5, 9, 15]},
    
    11: {'r': [6, 12, 16], 'b': [7, 17]},
    12: {'r': [6, 8, 16, 18], 'b': [7, 11, 13, 17]},
    13: {'r': [8, 12, 14, 18], 'b': [7, 9, 17, 19]},
    14: {'r': [8, 10, 18, 20], 'b': [9, 13, 15, 19]},
    15: {'r': [10, 14, 20], 'b': [9, 19]},
    
    16: {'r': [12, 22], 'b': [11, 17, 21]},
    17: {'r': [12, 16, 18, 22], 'b': [11, 13, 21, 23]},
    18: {'r': [12, 14, 22, 24], 'b': [13, 17, 19, 23]},
    19: {'r': [14, 18, 20, 24], 'b': [13, 15, 23, 25]},
    20: {'r': [14, 24], 'b': [15, 19, 25]},
    
    21: {'r': [16, 22], 'b': [17]},
    22: {'r': [16, 18], 'b': [17, 21, 23]},
    23: {'r': [18, 22, 24], 'b': [17, 19]},
    24: {'r': [18, 20], 'b': [19, 23, 25]},
    25: {'r': [20, 24], 'b': [19]},
}



def nfa_transition(state, char):
    """Devuelve los estados posibles a partir del estado actual según el carácter de entrada."""
    return boardstate.get(state, {}).get(char, [])


def find_all_paths(current_states, input_string, current_path, all_paths):
    """recursivamente todas las rutas con la cadena de entrada."""
    if not input_string:  # If the input string is empty, add the current path to all paths
        all_paths.append(current_path)
        return
    
    char = input_string[0]
    next_input = input_string[1:]
    
    for state in current_states:
        next_states = nfa_transition(state, char)
        for next_state in next_states:
            # Recursively find paths from the next state
            find_all_paths([next_state], next_input, current_path + [next_state], all_paths)


def nfa_find_all_paths(input_string, start_state=1):
    """Todas las rutas posibles"""
    current_states = [start_state]
    all_paths = []
    
    # Find all paths that the NFA can take for the input string
    find_all_paths(current_states, input_string, [start_state], all_paths)
    
    return all_paths


def write_paths_to_file(paths, filename):
    with open(filename, 'w') as file:
        for path in paths:
            file.write(','.join(map(str, path)) + '\n')


def verify_routes(filename="Bloque_1\\Tablero\\routes.txt", write_win_path="Bloque_1\\Tablero\\win_routes.txt", target_state=9):
    """Verificar si la ruta contiene el estado final"""
    valid_routes = []
    
    try:
        with open(filename, 'r') as file:
            routes = file.readlines()
            
            for route in routes:
                path = list(map(int, route.strip().split(',')))
                # Check if the target state is in the path
                if target_state in path:
                    # Create a new path without the occurrences of target state after the first one
                    new_path = []
                    found_target = False
                    
                    for state in path:
                        if state == target_state:
                            if not found_target:  # Keep the first occurrence
                                new_path.append(state)
                                found_target = True
                        else:
                            new_path.append(state)
                    
                    valid_routes.append(new_path)

        if valid_routes:
            # Write successful routes to a new file
            write_paths_to_file(valid_routes, write_win_path)
        else:
            print(f"No hay rutas que contenga la ruta final {target_state}.")
    
    except FileNotFoundError:
        print(f"Archivo '{filename}' no encontrado.")


def generar_cadena_rb():
    long_min = 5
    long_max = 10
    longitud = random.randint(long_min, long_max)
    return ''.join(random.choice(['r', 'b']) for _ in range(longitud))



#################################################################### GRAFICA ##################################################################################

def run_game_animation(ruta_j1, ruta_j2):
    positions = {
        1: (0, 4),  2: (1, 4),  3: (2, 4),  4: (3, 4),  5: (4, 4),
        6: (0, 3),  7: (1, 3),  8: (2, 3),  9: (3, 3), 10: (4, 3),
        11: (0, 2), 12: (1, 2), 13: (2, 2), 14: (3, 2), 15: (4, 2),
        16: (0, 1), 17: (1, 1), 18: (2, 1), 19: (3, 1), 20: (4, 1),
        21: (0, 0), 22: (1, 0), 23: (2, 0), 24: (3, 0), 25: (4, 0)
    }

    # Impares (negro), Pares (rojo)
    colors = {i: 'black' if i % 2 != 0 else 'red' for i in range(1, 26)}

    def leer_arrays_desde_txt(ruta_archivo):
        arrays = []
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                numeros_str = linea.strip().split(',')
                numeros = [int(num) for num in numeros_str if num]
                if numeros:
                    arrays.append(numeros)
        return arrays

    rutas_jugador1 = leer_arrays_desde_txt(ruta_j1)
    rutas_jugador2 = leer_arrays_desde_txt(ruta_j2)

    ruta_j1 = random.choice(rutas_jugador1)
    ruta_j2 = random.choice(rutas_jugador2)

    pos_j1 = ruta_j1[0]
    pos_j2 = ruta_j2[0]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(6, 6))

    # Dibujar las casillas del tablero
    for i in range(1, 26):
        x, y = positions[i]
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=colors[i]))
        ax.text(x, y, str(i), color='white', fontsize=16, ha='center', va='center')

    # Configurar los ejes
    ax.set_xticks(np.arange(-0.5, 5.5, 1))
    ax.set_yticks(np.arange(-0.5, 5.5, 1))
    ax.grid(True)
    plt.xlim(-0.5, 4.5)
    plt.ylim(-0.5, 4.5)
    ax.set_aspect('equal')

    # Inicializar las posiciones de los jugadores
    jugador1, = ax.plot([], [], 'bo', markersize=20, label='Jugador 1')
    jugador2, = ax.plot([], [], 'go', markersize=20, label='Jugador 2')
    titulo = ax.text(2, 5, "", ha="center", fontsize=14)

    # Estado inicial
    indice_j1 = 0
    indice_j2 = 0
    turno_j1 = True
    estado_final1 = 25
    estado_final2 = 21
    empate1 = False
    empate2 = False

    def encontrar_ruta_alternativa(rutas_disponibles, ruta_actual, indice_actual):
        for ruta in rutas_disponibles:
            if ruta[:indice_actual] == ruta_actual[:indice_actual] and len(ruta) > indice_actual:
                # Verifica si la ruta se desvía después del punto de conflicto
                if ruta[indice_actual] != ruta_actual[indice_actual]:
                    return ruta
        return None

    def actualizar(i):
        nonlocal pos_j1, pos_j2, turno_j1, indice_j1, indice_j2, ruta_j1, ruta_j2, empate1, empate2

        if turno_j1:  # Turno de Jugador 1
            if indice_j1 < len(ruta_j1):
                siguiente_pos_j1 = ruta_j1[indice_j1]
                if siguiente_pos_j1 == pos_j2:  # Colisión
                    nueva_ruta1 = encontrar_ruta_alternativa(rutas_jugador1, ruta_j1, indice_j1)
                    if nueva_ruta1 is None:
                        titulo.set_text(f"¡Colisión! Jugador 1 cede el turno")
                        turno_j1 = False
                        empate1 = True
                    else:
                        print(f"Ruta del jugador 1: {ruta_j1} -> nueva ruta jugador 1: {nueva_ruta1}")
                        ruta_j1 = nueva_ruta1
                        turno_j1 = True
                        titulo.set_text(f"¡Colisión! Jugador 1 cambia de ruta")
                else:
                    pos_j1 = siguiente_pos_j1
                    x_j1, y_j1 = positions[pos_j1]
                    jugador1.set_data([x_j1], [y_j1])
                    indice_j1 += 1
                    titulo.set_text(f"Jugador 1 se mueve a {pos_j1}")
                    turno_j1 = False

        else:  # Turno de Jugador 2
            if indice_j2 < len(ruta_j2):
                siguiente_pos_j2 = ruta_j2[indice_j2]
                if siguiente_pos_j2 == pos_j1:  # Colisión
                    nueva_ruta2 = encontrar_ruta_alternativa(rutas_jugador2, ruta_j2, indice_j2)
                    if nueva_ruta2 is None:
                        titulo.set_text(f"¡Colisión! Jugador 2 cede el turno")
                        turno_j1 = True
                        empate2 = True
                    else:
                        print(f"Ruta del jugador 2: {ruta_j2} -> nueva ruta jugador 2: {nueva_ruta2}")
                        ruta_j2 = nueva_ruta2
                        turno_j1 = False
                        titulo.set_text(f"¡Colisión! Jugador 2 cambia de ruta")
                else:
                    pos_j2 = siguiente_pos_j2
                    x_j2, y_j2 = positions[pos_j2]
                    jugador2.set_data([x_j2], [y_j2])
                    indice_j2 += 1
                    titulo.set_text(f"Jugador 2 se mueve a {pos_j2}")
                    turno_j1 = True

        
        if pos_j1 == estado_final1:
            print("¡Jugador 1 ganó!")
            ani.event_source.stop()
            print(f"Ruta ganadora: {ruta_j1}")
        elif pos_j2 == estado_final2:
            print("¡Jugador 2 ganó!")
            ani.event_source.stop()
            print(f"Ruta ganadora: {ruta_j2}")
        elif empate1 and empate2:
            print("Empate")
            ani.event_source.stop()
            print(f"Ruta J1: {ruta_j1}, Ruta J2: {ruta_j2}")

    def init():
        jugador1.set_data([], [])
        jugador2.set_data([], [])
        titulo.set_text("")
        return jugador1, jugador2, titulo

    # animación
    ani = FuncAnimation(fig, actualizar, frames=50, init_func=init, interval=1000, repeat=False)
    print(f"Ruta del jugador 1: {ruta_j1}")
    print(f"Ruta del jugador 2: {ruta_j2}")

    plt.legend()
    plt.title("Tablero jugadas en 5x5")
    plt.show()


#############################################################################  RED  ################################################################################

def red(archivo, mensaje, estado_fin):

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



    nx.draw(G, pos=posiciones, with_labels=False, node_size=800, node_color="lightblue", font_size=10, font_weight='bold', arrows=True)

    etiquetas = {nodo: f"{nodo[1]}" for nodo in G.nodes()}
    nx.draw_networkx_labels(G, pos=posiciones, labels=etiquetas, font_color='black', font_size=8)

    nodos_doble_circulo = [nodo for nodo in G.nodes() if nodo[1] == estado_fin]

        
    nx.draw(G, nodelist=nodos_doble_circulo, pos=posiciones, with_labels=False, node_size=600, node_color="cyan", font_size=10, font_weight='bold', arrows=True)

    
    
    plt.text(0.5, 0.95, mensaje, ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
    
    plt.title('Graph of Node Connections Across Positions')
    plt.axis('off')
    plt.show()

############################################################### MAIN ############################################################################################


def main():
    start_state1 = 1
    start_state2 = 5
    target1 = 25
    target2 = 21

    all_routes_player1 = "Bloque_1\\Tablero\\all_routes_player1.txt"
    all_routes_player2 = "Bloque_1\\Tablero\\all_routes_player2.txt"
    win_routes_player1 = "Bloque_1\\Tablero\\win_routes_player1.txt"
    win_routes_player2 = "Bloque_1\\Tablero\\win_routes_player2.txt"


    
    print("1. Modo automático")
    print("2. Modo manual")
    opcion = "1"
    opcion = input("Elige la opción: ")
    if opcion == "1":
        cadena = generar_cadena_rb()
        print(f"La cadena de movimiento generada es: {cadena}")
    elif opcion == "2":
        cadena = str(input("Escribe la cadena de movimiento (ex. rbbbrb): "))

    player1 = nfa_find_all_paths(cadena, start_state1)
    player2 = nfa_find_all_paths(cadena, start_state2)

    write_paths_to_file(player1, all_routes_player1)
    write_paths_to_file(player2, all_routes_player2)
    verify_routes(all_routes_player1, win_routes_player1, target1)
    verify_routes(all_routes_player2, win_routes_player2, target2)
    print(f"Escribiendo los movimientos '{cadena}' para ambos jugadores.")


    run_game_animation(win_routes_player1, win_routes_player2)
    red(all_routes_player1, "Red del jugador 1", target1)
    red(all_routes_player2, "Red del jugador 2", target2)

    
    

    


    

if __name__ == "__main__":
    main()
