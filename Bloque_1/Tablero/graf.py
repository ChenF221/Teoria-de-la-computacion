import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

# Definir la posición de los nodos en un tablero 3x3
positions = {
    1: (0, 2), 2: (1, 2), 3: (2, 2),
    4: (0, 1), 5: (1, 1), 6: (2, 1),
    7: (0, 0), 8: (1, 0), 9: (2, 0)
}

# Colores de los estados: Impares (negro), Pares (rojo)
colors = {i: 'black' if i % 2 != 0 else 'red' for i in range(1, 10)}

# Rutas del Jugador 1 y Jugador 2
rutas_jugador1 = [[1, 2, 5, 9], [1, 4, 5, 9]]
rutas_jugador2 = [[3, 2, 5, 7], [3, 6, 5, 7]]

# Función para seleccionar rutas alternativas
def buscar_ruta_alternativa(ruta_actual, rutas, camino_recorrido):
    # Filtrar rutas que sigan el camino recorrido
    posibles_rutas = [ruta for ruta in rutas if ruta[:len(camino_recorrido)] == camino_recorrido]
    if posibles_rutas:
        return random.choice(posibles_rutas)  # Elegir una al azar si hay coincidencias
    return None

# Seleccionar rutas al azar
ruta_j1 = random.choice(rutas_jugador1)
ruta_j2 = random.choice(rutas_jugador2)

# Definir las posiciones iniciales de los jugadores
pos_j1 = ruta_j1[0]
pos_j2 = ruta_j2[0]

# Crear el gráfico
fig, ax = plt.subplots(figsize=(6, 6))

# Dibujar las casillas del tablero 3x3, coloreadas completamente
for i in range(1, 10):
    x, y = positions[i]
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=colors[i]))  # Casilla completa
    ax.text(x, y, str(i), color='white', fontsize=16, ha='center', va='center')  # Numerar los nodos

# Configurar los ejes
ax.set_xticks(np.arange(-0.5, 3.5, 1))
ax.set_yticks(np.arange(-0.5, 3.5, 1))
ax.grid(True)
plt.xlim(-0.5, 2.5)
plt.ylim(-0.5, 2.5)
ax.set_aspect('equal')

# Colocar a los jugadores en sus posiciones iniciales
jugador1, = ax.plot([], [], 'bo', markersize=20, label='Jugador 1')  # Azul para Jugador 1
jugador2, = ax.plot([], [], 'go', markersize=20, label='Jugador 2')  # Verde para Jugador 2

# Alternar turnos
turno_j1 = random.choice([True, False])  # Randomizar quién inicia
titulo = ax.text(0, 3, "", ha="center", fontsize=14)

# Estado para los jugadores
indice_j1 = 0
indice_j2 = 0
ruta_actual_j2 = ruta_j2  # Ruta actual de Jugador 2
camino_j2 = [ruta_j2[0]]  # Para mantener el recorrido del Jugador 2

# Función de actualización de la animación
def actualizar(i):
    global pos_j1, pos_j2, turno_j1, indice_j1, indice_j2, ruta_actual_j2, camino_j2

    if turno_j1:  # Turno del Jugador 1
        if indice_j1 < len(ruta_j1):
            siguiente_pos_j1 = ruta_j1[indice_j1]
            # Verificar colisión con Jugador 2
            if siguiente_pos_j1 == pos_j2:
                titulo.set_text(f"¡Colisión! Jugador 1 espera")
            else:
                pos_j1 = siguiente_pos_j1
                x_j1, y_j1 = positions[pos_j1]
                jugador1.set_data([x_j1], [y_j1])
                indice_j1 += 1
                titulo.set_text(f"Jugador 1 se mueve a {pos_j1}")
        turno_j1 = False
    else:  # Turno del Jugador 2
        if indice_j2 < len(ruta_actual_j2):
            siguiente_pos_j2 = ruta_actual_j2[indice_j2]
            # Verificar colisión con Jugador 1
            if siguiente_pos_j2 == pos_j1:
                # Buscar una ruta alternativa que siga el mismo camino recorrido
                nueva_ruta = buscar_ruta_alternativa(ruta_actual_j2, rutas_jugador2, camino_j2)
                if nueva_ruta:
                    ruta_actual_j2 = nueva_ruta  # Cambiar de ruta
                    titulo.set_text(f"¡Colisión! Jugador 2 cambia de ruta")
                else:
                    titulo.set_text(f"¡Colisión! Jugador 2 cede el turno")
            else:
                pos_j2 = siguiente_pos_j2
                camino_j2.append(pos_j2)  # Actualizar el camino recorrido
                x_j2, y_j2 = positions[pos_j2]
                jugador2.set_data([x_j2], [y_j2])
                indice_j2 += 1
                titulo.set_text(f"Jugador 2 se mueve a {pos_j2}")
        turno_j1 = True

    # Verificar quién llegó al final
    if pos_j1 == ruta_j1[-1]:
        print("¡Jugador 1 ganó!")
        ani.event_source.stop()  # Detener la animación
    elif pos_j2 == ruta_actual_j2[-1]:
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
plt.title("Carrera en el tablero 3x3 con colisiones")
plt.show()
