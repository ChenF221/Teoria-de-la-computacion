import numpy as np
import matplotlib.pyplot as plt


def grafica(cadenas):
    plt.figure(figsize=(10, 6))

    posiciones = []
    cantidades = []
    colores = []

    for i, cadena in enumerate(cadenas):
        len_rojo = cadena.count('0')
        len_azul = cadena.count('1')

        if len_rojo > 0:
            posiciones.append(i)
            cantidades.append(len_rojo)
            colores.append('red')  # color para ceros

        if len_azul > 0:
            posiciones.append(i)
            cantidades.append(len_azul)
            colores.append('blue')  # color para unos

        if len_rojo == len_azul and len_rojo > 0:
            posiciones.append(i)
            cantidades.append(len_rojo)
            colores.append('purple')  # color para el mismo len de 1 y 0

    # graficar todos los puntos
    plt.scatter(posiciones, cantidades, color=colores)
    plt.scatter(0, 0, color='black')  # graficar cadena vacia

    plt.xlabel('Cadenas')
    plt.ylabel('Longitud de "0" y "1" (0=rojo, 1=azul)')
    plt.title('Grafica del universo binario')
    plt.grid(True)
    plt.show()


def grafica_log(cadenas):
    plt.figure(figsize=(10, 6))

    posiciones = []
    cantidades = []
    colores = []

    for i, cadena in enumerate(cadenas):
        len_rojo = cadena.count('0')
        len_azul = cadena.count('1')

        # Se aplican logaritmos, añadiendo un pequeño valor (1e-5) para evitar log(0)
        if len_rojo > 0:
            posiciones.append(i)
            cantidades.append(np.log10(len_rojo + 1e-5))  # logaritmo de la cantidad de ceros
            colores.append('red')  # color para ceros

        if len_azul > 0:
            posiciones.append(i)
            cantidades.append(np.log10(len_azul + 1e-5))  # logaritmo de la cantidad de unos
            colores.append('blue')  # color para unos

        if len_rojo == len_azul and len_rojo > 0:
            posiciones.append(i)
            cantidades.append(np.log10(len_rojo + 1e-5))  # logaritmo para igualdad de 1 y 0
            colores.append('purple')  # color para el mismo len de 1 y 0

    # Graficar todos los puntos
    plt.scatter(posiciones, cantidades, color=colores)
    plt.scatter(1, np.log10(1e-5), color='black')  # graficar cadena vacía

    plt.xlabel('Cadenas')
    plt.ylabel('log10 de la Longitud de "0" y "1" (0=rojo, 1=azul)')
    plt.title('Grafica logarítmica del universo binario')
    plt.grid(True)
    plt.show()


def leer_cadena(archivo):
    """Lee cadenas desde un archivo y devuelve una lista de cadenas."""
    with open(archivo, 'r') as f:
        cadenas = f.read().strip().splitlines()
    return cadenas


def main():

    cadenas = leer_cadena("Bloque_1\\Universo\\universo_n29.txt")
    opc = input("Presiona '1' para la grafica, o enter para terminar el programa: ")
    if opc == "1":
        grafica(cadenas)
        grafica_log(cadenas)
    print(f"Terminando el programa...")


if __name__ == "__main__":
    main()
