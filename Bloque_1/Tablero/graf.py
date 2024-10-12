import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation


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

ruta_j1 = "Bloque_1\\Tablero\\win_routes_player1.txt"
ruta_j2 = "Bloque_1\\Tablero\\win_routes_player2.txt"

rutas_jugador1 = leer_arrays_desde_txt(ruta_j1)
rutas_jugador2 = leer_arrays_desde_txt(ruta_j2)



ruta_j1 = random.choice(rutas_jugador1)
ruta_j2 = random.choice(rutas_jugador2)
#ruta_j2 = [5,4,3,7,11,16,21]


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
    global pos_j1, pos_j2, turno_j1, indice_j1, indice_j2, ruta_j1, ruta_j2, empate1, empate2
    

    if turno_j1:  # Turno de Jugador 1
        if indice_j1 < len(ruta_j1):
            siguiente_pos_j1 = ruta_j1[indice_j1]
            if siguiente_pos_j1 == pos_j2:  # Colisión
                #nueva_ruta1 = buscar_ruta_alternativa(rutas_jugador1, ruta_j1[:indice_j1+1], pos_j2)
                nueva_ruta1 = encontrar_ruta_alternativa(rutas_jugador1, ruta_j1, indice_j1)
                if nueva_ruta1 == None:
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
                #nueva_ruta2 = buscar_ruta_alternativa(rutas_jugador2, ruta_j2[:indice_j2+1], pos_j1)
                nueva_ruta2 = encontrar_ruta_alternativa(rutas_jugador2, ruta_j2, indice_j2)
                if nueva_ruta2 == None:
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
        

    # Verificar el estado final
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
