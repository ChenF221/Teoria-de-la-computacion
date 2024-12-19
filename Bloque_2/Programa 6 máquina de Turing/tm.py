"""
TM bien
"""
import random
from turtle import *
from time import sleep

class TuringMachine:
    def __init__(self, Q, Σ, Γ, δ, q0, B, F):
        self.Q = Q          # Conjunto de estados
        self.Σ = Σ          # Alfabeto de entrada
        self.Γ = Γ          # Alfabeto de la cinta
        self.δ = δ          # Función de transición (diccionario)
        self.q0 = q0        # Estado inicial
        self.B = B          # Símbolo en blanco
        self.F = F          # Conjunto de estados finales
        self.cinta = []     # Representación de la cinta (se inicializa con una cadena)
        self.cabezal = 0    # Posición del cabezal
        self.estado = q0    # Estado actual

    def cargar_cinta(self, cadena):
        # Inicializa la cinta 
        self.cinta = [self.B] + list(cadena) + [self.B]
        self.cabezal = 1

    def avanzar(self):
        if self.estado in self.F:
            return True  # La cadena es aceptada si estamos en un estado final
        
        len_cinta = sum(1 for _ in self.cinta)

        simbolo_actual = self.cinta[self.cabezal] if self.cabezal < len_cinta else self.B
        transicion = self.δ.get((self.estado, simbolo_actual))

        if not transicion:
            return False

        nuevo_estado, nuevo_simbolo, direccion = transicion
        self.cinta[self.cabezal] = nuevo_simbolo  # Escribir en la cinta
        self.estado = nuevo_estado  # Cambiar de estado

        # dirrecion
        if direccion == 'R':
            self.cabezal += 1
            if self.cabezal == len_cinta:  # Añadir blanco si se sale de la cinta
                self.cinta.append(self.B)
        elif direccion == 'L':
            self.cabezal -= 1
            if self.cabezal < 0:  # Añadir blanco a la izquierda si es necesario
                self.cinta.insert(0, self.B)
                self.cabezal = 0

        return None  # Continuar la ejecución

    def ejecutar_con_animacion(self, archivo_salida="salida.txt", mostrar_animacion=True):
        if mostrar_animacion:
            screen = Screen()
            screen.setup(width=800, height=400)
            screen.tracer(0)

            tr = Turtle()
            tr.hideturtle()
            tr.penup()

            def dibujar_cinta():
                tr.clear()
                x_inicio = -300
                for i, simbolo in enumerate(self.cinta):
                    x = x_inicio + i * 50
                    tr.setpos(x, 0)
                    tr.pendown()
                    for _ in range(4):
                        tr.forward(50)
                        tr.right(90)
                    tr.penup()
                    tr.setpos(x-25, -30)
                    tr.write(simbolo, align="center", font=("Arial", 16, "normal"))

                # Dibujar el cabezal el palo
                tr.setpos(x_inicio + self.cabezal * 50 - 25, 50)
                tr.write(f"{self.estado}", align="center", font=("Arial", 16, "bold"))
                tr.setpos(x_inicio + self.cabezal * 50 - 25, 40)
                tr.setheading(270)
                tr.pendown()
                tr.forward(30)
                tr.penup()

            dibujar_cinta()
            screen.update()

        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            while True:
                # Escribir el estado actual en el archivo
                cinta_con_estado = "".join(
                    self.cinta[:self.cabezal] +
                    [f"{self.estado}_"] +
                    self.cinta[self.cabezal:]
                )
                archivo.write(cinta_con_estado + "⊦\n")

                resultado = self.avanzar()
                if mostrar_animacion:
                    dibujar_cinta()
                    screen.update()
                    sleep(1)

                if resultado is not None:  # Terminar la ejecución
                    if mostrar_animacion:
                        screen.mainloop()
                    return resultado


def generarCadena(max_length=1000):
    asignacion = random.randint(1, max_length)
    cadena = ""
    if asignacion > 0:
        cadena += str(0) * asignacion  # Agregar ceros
        cadena += str(1) * asignacion  # Agregar unos
    return cadena



def main():
    Q = {'q0', 'q1', 'q2', 'q3', 'q4'}  # Conjunto de estados
    Σ = {'0', '1'}                      # Alfabeto de entrada
    Γ = {'0', '1', 'X', 'Y', 'B'}       # Alfabeto de la cinta
    B = 'B'                             # Blanco
    F = {'q4'}                          # Conjunto de estados finales
    δ = {                               # Función de transición
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', 'Y'): ('q3', 'Y', 'R'),
        ('q1', '0'): ('q1', '0', 'R'),
        ('q1', '1'): ('q2', 'Y', 'L'),
        ('q1', 'Y'): ('q1', 'Y', 'R'),
        ('q2', '0'): ('q2', '0', 'L'),
        ('q2', 'X'): ('q0', 'X', 'R'),
        ('q2', 'Y'): ('q2', 'Y', 'L'),
        ('q3', 'Y'): ('q3', 'Y', 'R'),
        ('q3', 'B'): ('q4', 'B', 'R'),
    }
    q0 = 'q0'  # Estado inicial


    tm = TuringMachine(Q, Σ, Γ, δ, q0, B, F)


    print("Seleccione una opción:")
    print("1. Ingresar la cadena manualmente")
    print("2. Generar una cadena automáticamente")

    opcion = int(input("Ingrese el número de su opción: "))

    if opcion == 1:
        cadena = input("Ingrese la cadena a evaluar (máximo 100,000 caracteres): ")
    elif opcion == 2:
        cadena = generarCadena()
        print(f"La cadena generada es: {cadena}")

    cadena_length = sum(1 for _ in cadena)
    if cadena_length <= 16:
        # Preguntar si se desea animación
        opcion_animacion = input("¿Desea mostrar la animación? (s/n): ").strip().lower()
        mostrar_animacion = opcion_animacion == 's'
    else:
        print("La cadena supera los 16 caracteres. No se puede animar.")
        return

    # Cargar una cadena de entrada
    #cadena = input("Ingrese la cadena a evaluar: ")
    tm.cargar_cinta(cadena)

    

    resultado = tm.ejecutar_con_animacion(archivo_salida="Bloque_2\\Programa 6 máquina de Turing\\salidaTM.txt", mostrar_animacion=mostrar_animacion)
    if resultado:
        print(f"\nLa cadena {cadena} ES aceptada. Los pasos se ha guardado en 'salidaTM.txt'.\n")
    else:
        print(f"\nLa cadena {cadena} NO es aceptada. Los pasos se ha guardado en 'salidaTM.txt'.\n")


if __name__ == "__main__":
    main()
