""" Universo de binarios """
import numpy as np
import matplotlib.pyplot as plt
import random

def generar_cadenas_binarias(n):
    cadenas = ['ε']
    
    for longitud in range(1, n + 1):
        max_num = 2 ** longitud
        for i in range(max_num):
            binario = bin(i)[2:]  # convertir el numero a binario y quitar el prefijo 0b
            binario = binario.zfill(longitud)  # rellenar ceros a la izquierda
            cadenas.append(binario)
    
    return cadenas


def guardar_en_archivo(cadenas, nombre_archivo="Bloque_1\\universo.txt"):
    with open(nombre_archivo, "w") as archivo:
        for cadena in cadenas:
            archivo.write(cadena + "\n")


def solicitar_valor():
    while True:
        try:
            n = input("Ingrese el valor de n >= 0 o presione Enter para un valor aleatorio: ")

            if n == "": # si el usuario no ingresa un valor
                n = random.randint(1, 10)
                print(f"Se ha generado un valor aleatorio: {n}")
                return n
            
            n = int(n)
            if n >= 0:
                return n
            else:
                print("Ingrese un valor entero positivo.")
        except ValueError:
            print("Valor no válido. Por favor, ingrese un número entero >= 0.")



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


def main():
    n = solicitar_valor()
    cadenas = generar_cadenas_binarias(n)
    guardar_en_archivo(cadenas)

    opc = input("Presiona '1' para la grafica, o enter para terminar el programa: ")
    if opc == "1":
        grafica(cadenas)
    print(f"Terminando el programa...")


if __name__ == "__main__":
    main()

