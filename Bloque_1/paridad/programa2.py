""" Protocolo con automata de paridad 0's y 1's """

import numpy as np
import matplotlib.pyplot as plt
import random
import time


class Automata:
    def __init__(self):
        self.estados = {'q0', 'q1', 'q2', 'q3'}
        self.estado_inicial = 'q0'
        self.estados_aceptacion = {'q0'}
        self.estado_actual = self.estado_inicial
        
        self.transiciones = {
            ('q0', '0'): 'q1',
            ('q0', '1'): 'q2',
            ('q1', '0'): 'q0',
            ('q1', '1'): 'q3',
            ('q2', '0'): 'q3',
            ('q2', '1'): 'q0',
            ('q3', '0'): 'q2',
            ('q3', '1'): 'q1',
        }

    def transitar(self, simbolo):
        if (self.estado_actual, simbolo) in self.transiciones:
            self.estado_actual = self.transiciones[(self.estado_actual, simbolo)]
        else:
            print("Transición invalida.")
            return False
        return True

    # acepta una cadena binaria y determina si es paridad de 0 y 1
    def procesar_cadena(self, cadena):
        self.estado_actual = self.estado_inicial
        for simbolo in cadena:
            if not self.transitar(simbolo):
                return False  # error en la transicion

        # si el estado final es uno de los estados de aceptacion
        if self.estado_actual in self.estados_aceptacion:
            return True
        else:
            return False
        

def generar_cadenas(n, nombre_archivo="Bloque_1\\cadenas_binarias.txt"):
    # n es numero de cadenas que quiere generar
    with open(nombre_archivo, "w") as archivo:
        for _ in range(n):
            cadena_binaria = ''.join(random.choice('01') for _ in range(64))
            archivo.write(cadena_binaria + '\n')
    print(f"Se han generado {n} cadenas binarias de 64 bits y guardado en {nombre_archivo}.")


def leer_cadenas(n, nombre_archivo="Bloque_1\\cadenas_binarias.txt"):
    with open(nombre_archivo, "r") as archivo:
        for i, linea in enumerate(archivo):
            if i == n:
                return linea.strip()
        raise IndexError("Índice fuera del rango del archivo.")
    

def escribir_true_false(bool, cadena):
    if bool == True:
        with open("Bloque_1\\cadenas_true.txt", "a") as archivo:
            archivo.write(cadena + '\n')
    else:
        with open("Bloque_1\\cadenas_false.txt", "a") as archivo:
            archivo.write(cadena + '\n')


def main():
    automata = Automata()

    num_cadenas = 500
    n = 1
    while True:
        # ready
        if n > 0.5:
            n = np.random.random()
            # data in
            generar_cadenas(num_cadenas)

            # send (2seconds)
            time.sleep(2)

            # ack (DFA)
            for i in range(num_cadenas):
                cadena = leer_cadenas(i)  # Leer cada cadena
                resultado = automata.procesar_cadena(cadena)  # Procesar la cadena con el autómata
                escribir_true_false(resultado, cadena)
        else:
            print("No se generaron nuevas cadenas.")
            break

    print("Terminando el programa...")


if __name__ == "__main__":
    main()


