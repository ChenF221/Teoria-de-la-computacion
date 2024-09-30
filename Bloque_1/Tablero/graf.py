import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

# Definir la posición de los nodos en un tablero 3x3
# positions = {
#     1: (0, 2), 2: (1, 2), 3: (2, 2),
#     4: (0, 1), 5: (1, 1), 6: (2, 1),
#     7: (0, 0), 8: (1, 0), 9: (2, 0)
# }

# 5x5
positions = {
    1: (0, 4),  2: (1, 4),  3: (2, 4),  4: (3, 4),  5: (4, 4),
    6: (0, 3),  7: (1, 3),  8: (2, 3),  9: (3, 3), 10: (4, 3),
   11: (0, 2), 12: (1, 2), 13: (2, 2), 14: (3, 2), 15: (4, 2),
   16: (0, 1), 17: (1, 1), 18: (2, 1), 19: (3, 1), 20: (4, 1),
   21: (0, 0), 22: (1, 0), 23: (2, 0), 24: (3, 0), 25: (4, 0)
}

# Colores de los estados: Impares (negro), Pares (rojo)
colors = {i: 'black' if i % 2 != 0 else 'red' for i in range(1, 26)}

# Rutas del Jugador 1 y Jugador 2
# rutas_jugador1 = [[1, 2, 5, 9], [1, 4, 5, 9]]
# rutas_jugador2 = [[3, 2, 5, 7], [3, 6, 5, 7]]


def leer_arrays_desde_txt(ruta_archivo):
    arrays = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            # Limpiar la línea de caracteres no deseados y dividir por comas
            numeros_str = linea.strip().split(',')
            # Convertir cada elemento a entero
            numeros = [int(num) for num in numeros_str]
            # Agregar el array de números a la lista
            arrays.append(numeros)
    return arrays


ruta_j1 = "Bloque_1\\Tablero\\win_routes_player1.txt"
ruta_j2 = "Bloque_1\\Tablero\\win_routes_player2.txt"

rutas_jugador1 = leer_arrays_desde_txt(ruta_j1)
rutas_jugador2 = leer_arrays_desde_txt(ruta_j2)


# Función para seleccionar rutas alternativas
def buscar_ruta_alternativa(ruta_actual, rutas, camino_recorrido):
    posibles_rutas = []
    for ruta in rutas:
        # Comprobar si la ruta alternativa comienza con el camino recorrido
        if ruta[:sum(1 for _ in camino_recorrido)] == camino_recorrido:
            posibles_rutas.append(ruta)
    
    if posibles_rutas:
        return random.choice(posibles_rutas)
    return None

# Seleccionar rutas al azar
ruta_j1 = random.choice(rutas_jugador1)
ruta_j2 = random.choice(rutas_jugador2)

# Definir las posiciones iniciales de los jugadores
pos_j1 = ruta_j1[0]
pos_j2 = ruta_j2[0]

# Tamaño de las rutas
tam_ruta_j1 = sum(1 for _ in ruta_j1)
tam_ruta_j2 = sum(1 for _ in ruta_j2)

# Crear el gráfico
fig, ax = plt.subplots(figsize=(6, 6))

# Dibujar las casillas del tablero 5x5
for i in range(1, 26):
    x, y = positions[i]
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=colors[i]))  # Casilla coloreada
    ax.text(x, y, str(i), color='white', fontsize=16, ha='center', va='center')  # Numerar los nodos

# Configurar los ejes
ax.set_xticks(np.arange(-0.5, 5.5, 1))
ax.set_yticks(np.arange(-0.5, 5.5, 1))
ax.grid(True)
plt.xlim(-0.5, 4.5)
plt.ylim(-0.5, 4.5)
ax.set_aspect('equal')

# Colocar a los jugadores en sus posiciones iniciales
jugador1, = ax.plot([], [], 'bo', markersize=20, label='Jugador 1')  # Azul para Jugador 1
jugador2, = ax.plot([], [], 'go', markersize=20, label='Jugador 2')  # Verde para Jugador 2

# Alternar turnos
turno_j1 = random.choice([True, False])  # Randomizar quién inicia
titulo = ax.text(2, 5, "", ha="center", fontsize=14)

# Estado para los jugadores
indice_j1 = 0
indice_j2 = 0
ruta_actual_j1 = ruta_j1
ruta_actual_j2 = ruta_j2  # Ruta actual de Jugador 2
camino_j1 = [ruta_j1[0]]  # Para mantener el recorrido del Jugador 2
camino_j2 = [ruta_j2[0]]  # Para mantener el recorrido del Jugador 2
tam_camino_j1 = 1  # Tamaño del camino recorrido por Jugador 2
tam_camino_j2 = 1  # Tamaño del camino recorrido por Jugador 2
estado_final1 = 25
estado_final2 = 21

# Función de actualización de la animación
def actualizar(i):
    global pos_j1, pos_j2, turno_j1, indice_j1, indice_j2, ruta_actual_j1, ruta_actual_j2, camino_j1, camino_j2, tam_camino_j1, tam_camino_j2

    if turno_j1:  # Turno del Jugador 1
        if indice_j1 < tam_ruta_j1:
            siguiente_pos_j1 = ruta_actual_j1[indice_j1]
            # Verificar colisión con Jugador 2
            if siguiente_pos_j1 == pos_j2:
                nueva_ruta1 = buscar_ruta_alternativa(ruta_j1, rutas_jugador1, camino_j1)
                if nueva_ruta1:
                    ruta_actual_j1 = nueva_ruta1  # Cambiar de ruta
                    titulo.set_text(f"¡Colisión! Jugador 1 cambia de ruta")
                else:
                    titulo.set_text(f"¡Colisión! Jugador 1 cede el turno")
            else:
                pos_j1 = siguiente_pos_j1
                camino_j1.append(pos_j1)
                tam_camino_j1 += 1
                x_j1, y_j1 = positions[pos_j1]
                jugador1.set_data([x_j1], [y_j1])
                indice_j1 += 1
                titulo.set_text(f"Jugador 1 se mueve a {pos_j1}")
        turno_j1 = False
    else:  # Turno del Jugador 2
        if indice_j2 < tam_ruta_j2:
            siguiente_pos_j2 = ruta_actual_j2[indice_j2]
            # Verificar colisión con Jugador 1
            if siguiente_pos_j2 == pos_j1:
                nueva_ruta2 = buscar_ruta_alternativa(ruta_j2, rutas_jugador2, camino_j2)
                if nueva_ruta2:
                    ruta_actual_j2 = nueva_ruta2  # Cambiar de ruta
                    titulo.set_text(f"¡Colisión! Jugador 2 cambia de ruta")
                else:
                    titulo.set_text(f"¡Colisión! Jugador 2 cede el turno")
            else:
                pos_j2 = siguiente_pos_j2
                camino_j2.append(pos_j2)  # Actualizar el camino recorrido
                tam_camino_j2 += 1  # Aumentar el tamaño del camino recorrido
                x_j2, y_j2 = positions[pos_j2]
                jugador2.set_data([x_j2], [y_j2])
                indice_j2 += 1
                titulo.set_text(f"Jugador 2 se mueve a {pos_j2}")
        turno_j1 = True

    # Verificar quién llegó al final
    if pos_j1 == estado_final1:
        print("¡Jugador 1 ganó!")
        ani.event_source.stop()  # Detener la animación
    elif pos_j2 == estado_final2:
        print("¡Jugador 2 ganó!")
        ani.event_source.stop()  # Detener la animación

# Función de inicialización de la animación
def init():
    jugador1.set_data([], [])
    jugador2.set_data([], [])
    titulo.set_text("")
    return jugador1, jugador2, titulo

# Crear la animación
ani = FuncAnimation(fig, actualizar, frames=50, init_func=init, interval=1000, repeat=False)

# Mostrar el gráfico con la animación
plt.legend()
plt.title("Tablero jugadas en 5x5")
plt.show()