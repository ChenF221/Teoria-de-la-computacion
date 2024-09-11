""" Protocolo con automata de paridad 0's y 1's """

import numpy as np
import matplotlib.pyplot as plt
import random


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


def main():
    generar_cadenas(500)
    automata = Automata()

    cadena1 = leer_cadenas(0)
    print(f"¿La cadena {cadena1} es paridad de 0's y 1's?:", automata.procesar_cadena(cadena1))


if __name__ == "__main__":
    main()


