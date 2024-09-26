import random
import matplotlib.pyplot as plt
import time
import networkx as nx
import pygame


tablaEstados = {
    1: {'B': [6], 'R': [2, 5]},
    2: {'B': [1, 3, 6], 'R': [5, 7]},
    3: {'B': [6, 8], 'R': [2, 4, 7]},
    4: {'B': [3, 8], 'R': [7]},
    5: {'B': [1, 6, 9], 'R': [2, 10]},
    6: {'B': [1, 3, 9, 11], 'R': [5, 2, 10, 7]},
    7: {'B': [3, 6, 8, 11], 'R': [2, 4, 10, 12]},
    8: {'B': [3, 11], 'R': [7, 4, 12]},
    9: {'B': [7, 14], 'R': [5, 10, 13]},
    10: {'B': [6, 9, 11, 14], 'R': [5,7,13,15]},
    11: {'B': [6, 8, 14, 16], 'R': [10,7,12,15]},
    12: {'B': [8, 11, 16], 'R': [7,15]},
    13: {'B': [9, 14], 'R': [10]},
    14: {'B': [9, 11], 'R': [13,10,15]},
    15: {'B': [14, 11, 16], 'R': [10,12]},
    16: {'B': [11], 'R': [15, 12]},
}

def combinacionesRutas(inicio, ruta):
    if not ruta:
        return [(inicio,)]
    
    primero, *nueva_ruta = ruta
    combinaciones = []
    for estado in tablaEstados[inicio][primero]:
        combinaciones.extend([(inicio,) + r for r in combinacionesRutas(estado, nueva_ruta)])
    return combinaciones

def guardarRutasEnArchivo(rutas, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for ruta in rutas:
            archivo.write(' -> '.join(map(str, ruta[1:])) + '\n')

def guardarRutasEnArchivo_terminan_en_16(rutas, nombre_archivo):
    rutas_terminadas_en_16 = [ruta for ruta in rutas if ruta[-1] == 16]
    if not rutas_terminadas_en_16:
        print("No se encontraron rutas que terminen en 16.")
        return
    with open(nombre_archivo, 'w') as archivo:
        for ruta in rutas_terminadas_en_16:
            archivo.write(' -> '.join(map(str, ruta[1:])) + '\n')

def guardarRutasEnArchivo_terminan_en_13(rutas, nombre_archivo):
    rutas_terminadas_en_13 = [ruta for ruta in rutas if ruta[-1] == 13]
    if not rutas_terminadas_en_13:
        print("No se encontraron rutas que terminen en 13.")
        return
    with open(nombre_archivo, 'w') as archivo:
        for ruta in rutas_terminadas_en_13:
            archivo.write(' -> '.join(map(str, ruta[1:])) + '\n')

def elegir_jugador_inicial():
    return random.choice([1, 2])

def numero_jugadores():
    return random.randint(1, 2)

def generar_ruta_aleatoria():
    longitud = random.randint(4, 10)
    acciones = ['B', 'R']
    ruta = ''.join(random.choice(acciones) for _ in range(longitud))
    return ruta

def reconfigurar_rutas(rutas_jugador1, rutas_jugador2, jugador_inicial):
    rutas_reconfiguradas_jugador1 = []
    rutas_reconfiguradas_jugador2 = []
    
    jugador1_length = 0
    jugador2_length = 0
    for ruta in rutas_jugador1:
        jugador1_length += 1
    for ruta in rutas_jugador2:
        jugador2_length += 1
    iteraciones = min(jugador1_length, jugador2_length)
    
    for i in range(iteraciones):
        ruta1 = list(rutas_jugador1[i])
        ruta2 = list(rutas_jugador2[i])
        
        turno_actual = jugador_inicial if i % 2 == 0 else 1
        
        ruta1_length = 0
        ruta2_length = 0
        for _ in ruta1:
            ruta1_length += 1
        for _ in ruta2:
            ruta2_length += 1
        min_length = min(ruta1_length, ruta2_length)
        
        for j in range(min_length):
            if ruta1[j] == ruta2[j]:
                if turno_actual == 1 and jugador_inicial == 1 or turno_actual == 2 and jugador_inicial == 1:
                    ruta1.insert(j, ruta1[j-1])
                else:
                    ruta2.insert(j, ruta2[j-1])
        
        rutas_reconfiguradas_jugador1.append(tuple(ruta1))
        rutas_reconfiguradas_jugador2.append(tuple(ruta2))
    
    return rutas_reconfiguradas_jugador1, rutas_reconfiguradas_jugador2

def leer_rutas_desde_archivo(nombre_archivo):
    rutas = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            ruta = list(map(int, linea.strip().split(' -> ')))
            rutas.append(ruta)
    return rutas

def obtenerRutasGanadoras(rutas, estado_deseado, longitud_maxima):
    rutas_limpias = []
    for ruta in rutas:
        count = 0
        for _ in ruta:
            count += 1
        if estado_deseado in ruta and count <= longitud_maxima:
            rutas_limpias.append(ruta)
    return rutas_limpias

def eliminar_lineas_hasta_ultimo_numero(linea, numero):
    partes = linea.strip().split(" -> ")
    partes_length = 0
    for _ in partes:
        partes_length += 1
        
    if partes_length >= 4:
        indice_ultimo_numero = None
        for i in range(partes_length - 1, -1, -1):
            if partes[i] == numero:
                indice_ultimo_numero = i
                break
        if indice_ultimo_numero is not None:
            nueva_linea = " ".join(partes[:indice_ultimo_numero+1]) + "\n"
            nueva_linea_length = 0
            for _ in nueva_linea:
                nueva_linea_length += 1
            if nueva_linea_length >= 5:
                return nueva_linea
    return ""

def limpiar(archivo_entrada, archivo_salida, numero, max_length):
    lineas_unicas = set()

    with open(archivo_entrada, 'r') as archivo_lectura, open(archivo_salida, 'w') as archivo_escritura:
        for linea in archivo_lectura:
            nueva_linea = eliminar_lineas_hasta_ultimo_numero(linea, numero)
            if nueva_linea and nueva_linea not in lineas_unicas:
                archivo_escritura.write(nueva_linea)
                lineas_unicas.add(nueva_linea)

    # Leer el archivo y almacenar las líneas en una lista
    with open(archivo_salida, "r") as file:
        lines = file.readlines()

    if lines:  # Verificar si hay líneas en el archivo
        # Filtrar las líneas que tienen la longitud máxima
        filtered_lines = []
        for line in lines:
            line_length = 0
            for _ in line.split():
                line_length += 1
            if line_length == max_length:
                filtered_lines.append(line)

        # Escribir las líneas filtradas de nuevo al archivo
        with open(archivo_salida, "w") as file:
            file.writelines(filtered_lines)
    else:
        print("No hay rutas ganadoras")



        

######################################################################  GráficasAjedrez #####################################################################


def graficar_red_desde_archivo(nombre_archivo, inicio):
    # Crear un grafo dirigido
    G = nx.DiGraph()

    # Leer el archivo y agregar las rutas al grafo
    with open(nombre_archivo, 'r') as file:
        for line in file:
            ruta = list(map(int, line.strip().split(" -> ")))
            ruta.insert(0, inicio)
            for origen, destino in zip(ruta, ruta[1:]):
                G.add_edge(origen, destino)

    # Graficar el grafo
    pos = nx.spring_layout(G, seed=42)

    # Dibujar los nodos
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', edgecolors='black')

    # Dibujar las aristas
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color='gray')

    # Dibujar las etiquetas de los nodos
    labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')

    plt.title('Red de estados')
    plt.axis('off')  # Desactivar los ejes
    plt.show()
    #plt.gcf().canvas.manager.window.after(5000, plt.close)


# Dimensiones de la pantalla
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# Tamaño de cada cuadrado del tablero
SQUARE_SIZE = 100

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Coordenadas de los estados en el tablero de ajedrez
state_coordinates = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (3, 0),
    5: (0, 1),
    6: (1, 1),
    7: (2, 1),
    8: (3, 1),
    9: (0, 2),
    10: (1, 2),
    11: (2, 2),
    12: (3, 2),
    13: (0, 3),
    14: (1, 3),
    15: (2, 3),
    16: (3, 3),
}

def dibujartablero(screen):
    # Dibujar el tablero de ajedrez
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                color = BLACK
            else:
                color = RED
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def dibujarpieza(screen, color, position):
    # Dibujar una pieza en la posición dada
    x, y = position
    pygame.draw.circle(screen, color, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), 30)

def animarRutas2Jugadores(screen, route_red, route_blue):
    if route_red is None or route_blue is None:
        print("No se puede animar dado que no hay rutas ganadoras.")
        return
    
    i_red = 0
    i_blue = 0
    
    route_red_length = 0
    for _ in route_red:
        route_red_length += 1
    
    route_blue_length = 0
    for _ in route_blue:
        route_blue_length += 1
    
    while i_red < route_red_length or i_blue < route_blue_length:
        screen.fill(WHITE)
        dibujartablero(screen)
        
        if i_red < route_red_length:
            dibujarpieza(screen, WHITE, state_coordinates[route_red[i_red]])
            i_red += 1
            pygame.display.flip()
            time.sleep(0.5)
        
        if i_blue < route_blue_length:
            dibujarpieza(screen, BLUE, state_coordinates[route_blue[i_blue]])
            i_blue += 1
            pygame.display.flip()
            time.sleep(2)

def animarRuta1jugador(screen, route_red):
    if route_red is None:
        print("No se puede animar dado que no hay rutas ganadoras.")
        return
    i_red = 0
    
    route_red_length = 0
    for _ in route_red:
        route_red_length += 1
    
    while i_red < route_red_length:
        screen.fill(WHITE)
        dibujartablero(screen)
        
        if i_red < route_red_length:
            dibujarpieza(screen, WHITE, state_coordinates[route_red[i_red]])
            i_red += 1
            pygame.display.flip()
            time.sleep(2)

def animarrutaGanadora(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        if not first_line:
            print("No hay rutas ganadoras.")
            return None
        route = [int(num) for num in first_line.split()]
    route.insert(0, 1)  # Agregar el valor 1 al principio de la lista
    return route

def obtenerRutaGanador1jugador(filename):
    with open(filename, 'r') as file:
        route_str = file.readline().strip()
        if not route_str:
            print("No hay rutas ganadoras.")
            return None
        route_str_list = route_str.split(" -> ")  # Divide la cadena en una lista
        route = [int(num) for num in route_str_list]  # Convierte los elementos a enteros
    route.insert(0, 1)  # Agrega el valor 1 al principio de la lista
    return route

def obtenerRutaGanadora2jugador(filename):
    with open(filename, 'r') as file:
        route_str = file.readline().strip()
        if not route_str:
            print("No hay rutas ganadoras.")
            return None
        route_str_list = route_str.split(" -> ")  # Divide la cadena en una lista
        route = [int(num) for num in route_str_list]  # Convierte los elementos a enteros
    route.insert(0, 4)  # Agregar el valor 4 al principio de la lista
    return route

def main():
    nombre_archivo1 = 'rutas1.txt'
    nombre_archivo2 = 'rutas2.txt'
    nombre_archivo1_1 = 'rutas1_16.txt'
    nombre_archivo1_2 = 'rutas2_13.txt'
    nombre_archivo1_1_3 = 'rutas1_16limpias.txt'
    nombre_archivo1_2_3 = 'rutas2_13limpias.txt'
    nombre_archivo1_reconfigurado = 'rutas1_reconfiguradas.txt'
    nombre_archivo2_reconfigurado = 'rutas2_reconfiguradas.txt'

    print("1. Modo automático")
    print("2. Modo manual")
    opcion="1"
    opcion=input("Elige la opción: ")
    if opcion == "1":

        ruta = generar_ruta_aleatoria()  # Genera una ruta aleatoria
        print("Ruta generada automáticamente:", ruta)
        numero = numero_jugadores()
        print(f"Número de jugadores: {numero}")
        if numero == 2:
            jugador_inicial = elegir_jugador_inicial()
            otro_jugador = 2 if jugador_inicial == 1 else 1  # El otro jugador será el que no inició

            resultado1 = combinacionesRutas(1, ruta)
            resultado2 = combinacionesRutas(4, ruta)

            guardarRutasEnArchivo(resultado1, nombre_archivo1)
            guardarRutasEnArchivo(resultado2, nombre_archivo2)

            # Limpiar las rutas antes de guardarlas en los archivos 1_16 y 2_13

            rutas_limpias_jugador1_16 = obtenerRutasGanadoras(resultado1, 16, 10)  # Por ejemplo, solo rutas que contienen el estado 16 y tienen una longitud máxima de 20
            rutas_limpias_jugador2_13 = obtenerRutasGanadoras(resultado2, 13, 10)  # Similarmente, para el estado 13

            guardarRutasEnArchivo(rutas_limpias_jugador1_16, nombre_archivo1_1)
            guardarRutasEnArchivo(rutas_limpias_jugador2_13, nombre_archivo1_2)

            # Reconfigurar las rutas si es necesario, comparando las rutas de ambos jugadores
            resultado1_reconfigurado, resultado2_reconfigurado = reconfigurar_rutas(rutas_limpias_jugador1_16, rutas_limpias_jugador2_13, jugador_inicial)

            guardarRutasEnArchivo(resultado1_reconfigurado, nombre_archivo1_reconfigurado)
            guardarRutasEnArchivo(resultado2_reconfigurado, nombre_archivo2_reconfigurado)

            if ruta[-1] == 'B':
                # Filtrar para el número 13
                limpiar(nombre_archivo1_2, nombre_archivo1_2_3, '13', 5)
                # Filtrar para el número 16
                limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 6)
            elif ruta[-1] == 'R':
                # Filtrar para el número 13
                limpiar(nombre_archivo1_2, nombre_archivo1_2_3, '13', 6)
                # Filtrar para el número 16
                limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 5)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en'{nombre_archivo1}'.")
            print(f"Se han guardado las rutas en el archivo del jugador 2 en'{nombre_archivo2}'.")

            graficar_red_desde_archivo(nombre_archivo1, 1)
            graficar_red_desde_archivo(nombre_archivo2, 4)

            print(f"Inicia el jugador: {jugador_inicial}\n")

            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Tablero de Ajedrez")

            # Leer la primera ruta desde el archivo
            first_route = obtenerRutaGanador1jugador("rutas1_reconfiguradas.txt")
            second_route = obtenerRutaGanadora2jugador("rutas2_reconfiguradas.txt")
            print("Las rutas a animar son: ","Jugador 1:", first_route, "Jugador 2:", second_route)
            animarRutas2Jugadores(screen, first_route, second_route)

            # Salir del programa después de la animación
            pygame.quit()

            if first_route is not None and first_route[-1] == 16:
                print("El jugador ganador es el 1")
            elif second_route is not None and second_route[-1] == 13:
                print("El jugador ganador es el 2")
            else:
                print("No se encontró un jugador ganador")
            #sys.exit()

        elif numero == 1:

            resultado1 = combinacionesRutas(1, ruta)

            guardarRutasEnArchivo(resultado1, nombre_archivo1)

            # Limpiar las rutas antes de guardarlas en los archivos 1_16 y 2_13
            rutas_limpias_jugador1_16 = obtenerRutasGanadoras(resultado1, 16, 10)  # Por ejemplo, solo rutas que contienen el estado 16 y tienen una longitud máxima de 20

            guardarRutasEnArchivo(rutas_limpias_jugador1_16, nombre_archivo1_1)
            limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 6)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en'{nombre_archivo1}'.")

            graficar_red_desde_archivo(nombre_archivo1, 1)
            
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Tablero de Ajedrez")

            # Leer la primera ruta desde el archivo
            first_route = animarrutaGanadora("rutas1_16limpias.txt")
            print(first_route)
            animarRuta1jugador(screen, first_route)

            # Salir del programa después de la animación
            pygame.quit()
            #sys.exit()

    elif opcion == "2":
        print("1. Ruta de forma manual")
        print("2. Ruta de forma automatica")
        opcion=input("Elige la opción: ")
        if opcion == "1":
            ruta = input("Dame la ruta: ")
        elif opcion == "2":
            ruta = generar_ruta_aleatoria()  # Genera una ruta aleatoria
            print("Ruta generada automáticamente:", ruta)
        numero = input("Dame el número de jugadores: ")
        if numero == "2":
            jugador_inicial = elegir_jugador_inicial()
            otro_jugador = 2 if jugador_inicial == 1 else 1  # El otro jugador será el que no inició

            
            resultado1 = combinacionesRutas(1, ruta)
            resultado2 = combinacionesRutas(4, ruta)

            guardarRutasEnArchivo(resultado1, nombre_archivo1)
            guardarRutasEnArchivo(resultado2, nombre_archivo2)

            # Limpiar las rutas antes de guardarlas en los archivos 1_16 y 2_13

            rutas_limpias_jugador1_16 = obtenerRutasGanadoras(resultado1, 16, 10)  # Por ejemplo, solo rutas que contienen el estado 16 y tienen una longitud máxima de 20
            rutas_limpias_jugador2_13 = obtenerRutasGanadoras(resultado2, 13, 10)  # Similarmente, para el estado 13

            guardarRutasEnArchivo(rutas_limpias_jugador1_16, nombre_archivo1_1)
            guardarRutasEnArchivo(rutas_limpias_jugador2_13, nombre_archivo1_2)

            # Reconfigurar las rutas si es necesario, comparando las rutas de ambos jugadores
            resultado1_reconfigurado, resultado2_reconfigurado = reconfigurar_rutas(rutas_limpias_jugador1_16, rutas_limpias_jugador2_13, jugador_inicial)

            guardarRutasEnArchivo(resultado1_reconfigurado, nombre_archivo1_reconfigurado)
            guardarRutasEnArchivo(resultado2_reconfigurado, nombre_archivo2_reconfigurado)

            if ruta[-1] == 'B':
                # Filtrar para el número 13
                limpiar(nombre_archivo1_2, nombre_archivo1_2_3, '13', 5)
                # Filtrar para el número 16
                limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 6)
            elif ruta[-1] == 'R':
                # Filtrar para el número 13
                limpiar(nombre_archivo1_2, nombre_archivo1_2_3, '13', 6)
                # Filtrar para el número 16
                limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 5)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en'{nombre_archivo1}'.")
            print(f"Se han guardado las rutas en el archivo del jugador 2 en'{nombre_archivo2}'.")

            graficar_red_desde_archivo(nombre_archivo1, 1)
            graficar_red_desde_archivo(nombre_archivo2, 4)

            print(f"Inicia el jugador: {jugador_inicial}\n")

            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Tablero de Ajedrez")

            # Leer la primera ruta desde el archivo
            first_route = obtenerRutaGanador1jugador("rutas1_reconfiguradas.txt")
            second_route = obtenerRutaGanadora2jugador("rutas2_reconfiguradas.txt")
            print("Las rutas a animar son: ","Jugador 1:", first_route, "Jugador 2:", second_route)
            animarRutas2Jugadores(screen, first_route, second_route)

            # Salir del programa después de la animación
            pygame.quit()
            if first_route is not None and first_route[-1] == 16:
                print("El jugador ganador es el 1")
            elif second_route is not None and second_route[-1] == 13:
                print("El jugador ganador es el 2")
            else:
                print("No se encontró un jugador ganador")
            #sys.exit()

        elif numero == "1":

            resultado1 = combinacionesRutas(1, ruta)
            guardarRutasEnArchivo(resultado1, nombre_archivo1)

            # Limpiar las rutas antes de guardarlas en los archivos 1_16 y 2_13
            rutas_limpias_jugador1_16 = obtenerRutasGanadoras(resultado1, 16, 10)  # Por ejemplo, solo rutas que contienen el estado 16 y tienen una longitud máxima de 20

            guardarRutasEnArchivo(rutas_limpias_jugador1_16, nombre_archivo1_1)
            limpiar(nombre_archivo1_1, nombre_archivo1_1_3, '16', 6)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en'{nombre_archivo1}'.")

            graficar_red_desde_archivo(nombre_archivo1, 1)
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Tablero de Ajedrez")

            # Leer la primera ruta desde el archivo
            first_route = animarrutaGanadora("rutas1_16limpias.txt")
            print(first_route)
            animarRuta1jugador(screen, first_route)

            # Salir del programa después de la animación
            pygame.quit()
            #sys.exit()


if __name__ == "__main__":
    main()
