import random
import matplotlib.pyplot as plt
import time
import networkx as nx
import pygame


tablaEstados = {
    1: {'r': [2, 4], 'b': [5]},
    2: {'r': [4, 6], 'b': [1, 3, 5]},
    3: {'r': [2, 6], 'b': [5]},
    4: {'r': [2, 8], 'b': [1, 5, 7]},
    5: {'r': [2, 4, 6, 8], 'b': [1, 3, 7, 9]},
    6: {'r': [2, 8], 'b': [3, 5, 9]},
    7: {'r': [4, 8], 'b': [5]},
    8: {'r': [4, 6], 'b': [5, 7, 9]},
    9: {'r': [6, 8], 'b': [5]}
}


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
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 2),
    8: (1, 2),
    9: (2, 2),
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
            archivo.write(' '.join(map(str, ruta[1:])) + '\n')

# guardar rutas en archivo para el jugador 1
def guardarRutasEnArchivo_jugador1(rutas, nombre_archivo, estado_final = 9):
    rutas_terminadas_jugador1 = [ruta for ruta in rutas if ruta[-1] == estado_final]
    if not rutas_terminadas_jugador1:
        print(f"No se encontraron rutas que terminen en {estado_final}.")
        return
    with open(nombre_archivo, 'w') as archivo:
        for ruta in rutas_terminadas_jugador1:
            archivo.write(' '.join(map(str, ruta[1:])) + '\n')


# guardar rutas en archivo para el jugador 2
def guardarRutasEnArchivo_jugador2(rutas, nombre_archivo, estado_final = 7):
    rutas_terminadas_jugador2 = [ruta for ruta in rutas if ruta[-1] == estado_final]
    if not rutas_terminadas_jugador2:
        print(f"No se encontraron rutas que terminen en {estado_final}.")
        return
    with open(nombre_archivo, 'w') as archivo:
        for ruta in rutas_terminadas_jugador2:
            archivo.write(' '.join(map(str, ruta[1:])) + '\n')

def elegir_jugador_inicial():
    return random.choice([1, 2])

def numero_jugadores():
    return random.randint(1, 2)



def generar_ruta_aleatoria():
    longitud = random.randint(4, 10)
    acciones = ['r', 'b']
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


###
def leer_rutas_desde_archivo(nombre_archivo):
    rutas = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            ruta = list(map(int, linea.strip().split(' ')))
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
    partes = linea.strip()
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


def main():
    nombre_archivo1 = 'Bloque_1\\Tablero\\rutas_jugador1.txt'
    nombre_archivo2 = 'Bloque_1\\Tablero\\rutas_jugador2.txt'
    nombre_archivo1_reconfigurado = 'Bloque_1\\Tablero\\rutas1_reconfiguradas.txt'
    nombre_archivo2_reconfigurado = 'Bloque_1\\Tablero\\rutas2_reconfiguradas.txt'

    print("1. Modo automático")
    print("2. Modo manual")
    opcion = input("Elige la opción: ")

    if opcion == "1":
        ruta = generar_ruta_aleatoria()  # Genera una ruta aleatoria
        print("Ruta generada automáticamente:", ruta)
        numero = numero_jugadores()
        print(f"Número de jugadores: {numero}")

        if numero == 2:
            jugador_inicial = elegir_jugador_inicial()
            otro_jugador = 2 if jugador_inicial == 1 else 1  # El otro jugador será el que no inició

            # Generar combinaciones de rutas para ambos jugadores
            resultado1 = combinacionesRutas(1, ruta)
            resultado2 = combinacionesRutas(3, ruta)

            # Guardar rutas en archivos
            guardarRutasEnArchivo(resultado1, nombre_archivo1)
            guardarRutasEnArchivo(resultado2, nombre_archivo2)

            # Reconfigurar las rutas si es necesario, comparando las rutas de ambos jugadores
            resultado1_reconfigurado, resultado2_reconfigurado = reconfigurar_rutas(resultado1, resultado2, jugador_inicial)

            guardarRutasEnArchivo(resultado1_reconfigurado, nombre_archivo1_reconfigurado)
            guardarRutasEnArchivo(resultado2_reconfigurado, nombre_archivo2_reconfigurado)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en '{nombre_archivo1}'.")
            print(f"Se han guardado las rutas en el archivo del jugador 2 en '{nombre_archivo2}'.")

        elif numero == 1:
            # Generar combinaciones de rutas para el jugador 1
            resultado1 = combinacionesRutas(1, ruta)
            guardarRutasEnArchivo(resultado1, nombre_archivo1)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en '{nombre_archivo1}'.")

    elif opcion == "2":
        print("1. Ruta de forma automática")
        print("2. Ruta de forma manual")
        opcion = input("Elige la opción: ")
        
        if opcion == "1":
            ruta = generar_ruta_aleatoria()  # Genera una ruta aleatoria
            print("Ruta generada automáticamente:", ruta)
        elif opcion == "2":
            ruta = input("Dame la ruta: ")
            

        numero = input("Dame el número de jugadores: ")

        if numero == "2":
            jugador_inicial = elegir_jugador_inicial()
            otro_jugador = 2 if jugador_inicial == 1 else 1  # El otro jugador será el que no inició

            # Generar combinaciones de rutas para ambos jugadores
            resultado1 = combinacionesRutas(1, ruta)
            resultado2 = combinacionesRutas(4, ruta)

            # Guardar rutas en archivos
            guardarRutasEnArchivo(resultado1, nombre_archivo1)
            guardarRutasEnArchivo(resultado2, nombre_archivo2)

            # Reconfigurar las rutas si es necesario, comparando las rutas de ambos jugadores
            resultado1_reconfigurado, resultado2_reconfigurado = reconfigurar_rutas(resultado1, resultado2, jugador_inicial)

            guardarRutasEnArchivo(resultado1_reconfigurado, nombre_archivo1_reconfigurado)
            guardarRutasEnArchivo(resultado2_reconfigurado, nombre_archivo2_reconfigurado)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en '{nombre_archivo1}'.")
            print(f"Se han guardado las rutas en el archivo del jugador 2 en '{nombre_archivo2}'.")

        elif numero == "1":
            # Generar combinaciones de rutas para el jugador 1
            resultado1 = combinacionesRutas(1, ruta)
            guardarRutasEnArchivo(resultado1, nombre_archivo1)

            print(f"Se han guardado las rutas en el archivo del jugador 1 en '{nombre_archivo1}'.")


if __name__ == "__main__":
    main()

