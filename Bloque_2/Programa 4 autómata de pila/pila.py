import random
from turtle import *
from time import *


# Clase NodoPila que representa un nodo en la estructura de pila
class NodoPila:
    def __init__(self, dato):
        self.dato = dato  # Almacena el valor del nodo
        self.siguiente = None  # Referencia al siguiente nodo (por defecto es None)


# Clase EstructuraPila que implementa una pila utilizando la clase NodoPila
class EstructuraPila:
    def __init__(self):
        self.tope = None  # El tope de la pila inicia vacío

    def insertar(self, dato):
        """Inserta un dato en la pila"""
        if self.tope is None:  # Si la pila está vacía
            self.tope = NodoPila(dato)  # Crear un nuevo nodo como tope
            return
        
        # Si la pila no está vacía, crear un nuevo nodo y agregarlo al principio
        nuevo_nodo = NodoPila(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo

    def quitar(self):
        """Quita el elemento del tope de la pila"""
        if self.tope is None:
            return "Z"  # Si la pila está vacía, retornamos el símbolo Z (caracter de aceptación)

        # Si la pila no está vacía, eliminar el nodo del tope
        temp = self.tope
        self.tope = self.tope.siguiente
        return temp.dato


# Función que genera una cadena de caracteres aleatoria que consiste en ceros y unos
def generarCadena():
    asignacion = random.randint(1, 10000)  # Asignamos un valor aleatorio para la longitud de la cadena
    cadena = ""
    if asignacion != 0:
        cadena += str(0) * asignacion  # Agregar ceros
        cadena += str(1) * asignacion  # Agregar unos
    return cadena


# Función para animar el autómata que valida la cadena
def animarAutomata(cadena):
    pila = EstructuraPila()  # Crear una nueva pila para el autómata

    # Configurar la velocidad de la animación y la posición de inicio de la tortuga
    speed(8)
    penup(), setpos(-100, 100), pendown()

    # Dibuja un rectángulo con un color alterno para representar el autómata
    begin_fill()
    for lado in range(4):
        if lado % 2 == 0:
            fillcolor("yellow")
            pencolor("black")
        else:
            fillcolor("green")
            pencolor("black")
        forward(100)
        right(90)
    end_fill()

    # Dibuja las flechas para indicar el inicio y fin del autómata
    penup(), setpos(-50, 100), pendown()
    setpos(-50, 150), setpos(-45, 140), setpos(-50, 150), setpos(-55, 140)

    penup(), setpos(-50, 0), pendown()
    setpos(-50, -50), setpos(-45, -40), setpos(-50, -50), setpos(-55, -40)
    hideturtle()  # Esconde la tortuga para no mostrarla mientras dibujamos

    turtle = Turtle()  # Crea una nueva tortuga para escribir el estado

    # Inicializa las variables de la cadena que se evalúa
    cadenaMod = cadena
    cadenaPila = "Z"  # El símbolo Z indica el fondo de la pila (inicio)
    resultado = "(q, " + cadenaMod + ", " + cadenaPila + ")⊦\n"

    # Muestra la cadena inicial en la pantalla
    turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()
    turtle.write(cadenaMod, False, align="left", font=("Lucida Console", 20))

    # Si el primer carácter es '0', mostramos el estado 'q'
    if cadenaMod[0:1] == '0':
        turtle.penup(), turtle.setpos(-50, 40), turtle.pendown()
        turtle.write('q', False, align="center", font=("Lucida Console", 20))

    # Dibuja la pila (con el fondo 'Z')
    cont = -80
    for letra in cadenaPila:
        turtle.penup(), turtle.setpos(-50, cont), turtle.pendown()
        turtle.write(letra, False, align="center", font=("Lucida Console", 20))
        cont -= 20
    sleep(1)

    # Verifica si la cadena comienza con un '1', en cuyo caso no es aceptada
    if cadenaMod[0:1] == '1':
        resultado = "La cadena no es aceptada"
    else:
        turtle.clear()  # Borra la pantalla para la nueva animación
        estado = 0  # Estado inicial del autómata

        # Itera a través de cada símbolo de la cadena
        for i in cadena:
            turtle.clear()
            match estado:
                case 0:
                    if int(i) == 0:  # Si el carácter es '0', apilar un 'x'
                        pila.insertar("x")
                        cadenaMod = cadenaMod[1:]
                        cadenaPila = "X" + cadenaPila
                        resultado += "(q, " + cadenaMod + ", " + cadenaPila + ")⊦\n"
                    elif int(i) == 1:  # Si el carácter es '1', desencolar un 'x'
                        cadenaMod = cadenaMod[1:]
                        cadenaPila = cadenaPila[1:]
                        if cadenaMod == "":
                            resultado += "(p, ε, " + cadenaPila + ")⊦\n"
                            cadenaMod = "ε"
                        else:
                            resultado += "(p, " + cadenaMod + ", " + cadenaPila + ")⊦\n"
                        pila.quitar()
                        estado = 1  # Cambia al estado 1
                case 1:
                    if int(i) == 1:  # Si el carácter es '1', desencolar un elemento
                        dato = pila.quitar()
                        if dato == "Z":  # Si encontramos el fondo de la pila, la cadena es aceptada
                            turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()
                            turtle.write(cadenaMod, False, align="left", font=("Lucida Console", 20))
                            turtle.penup(), turtle.setpos(-50, 40), turtle.pendown()
                            turtle.write('f', False, align="center", font=("Lucida Console", 20))
                            cont = -80
                            for letra in cadenaPila:
                                turtle.penup(), turtle.setpos(-50, cont), turtle.pendown()
                                turtle.write(letra, False, align="center", font=("Lucida Console", 20))
                                cont -= 20
                            sleep(1)
                            break

                        cadenaMod = cadenaMod[1:]
                        cadenaPila = cadenaPila[1:]
                        if cadenaMod == "":
                            resultado += "(p, ε, " + cadenaPila + ")⊦\n"
                            cadenaMod = "ε"
                        else:
                            resultado += "(p, " + cadenaMod + ", " + cadenaPila + ")⊦\n"
                    else:  # Si el carácter no es '1', la cadena no es aceptada
                        turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()
                        turtle.write(cadenaMod, False, align="left", font=("Lucida Console", 20))
                        turtle.penup(), turtle.setpos(-50, 40), turtle.pendown()
                        turtle.write('f', False, align="center", font=("Lucida Console", 20))
                        cont = -80
                        for letra in cadenaPila:
                            turtle.penup(), turtle.setpos(-50, cont), turtle.pendown()
                            turtle.write(letra, False, align="center", font=("Lucida Console", 20))
                            cont -= 20
                        sleep(1)
                        break

            # Actualiza la animación con los nuevos valores
            turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()
            turtle.write(cadenaMod, False, align="left", font=("Lucida Console", 20))
            turtle.penup(), turtle.setpos(-50, 40), turtle.pendown()

            index = 0
            if cadenaMod[index] == '0':
                turtle.write('q', False, align="center", font=("Lucida Console", 20))
                index += 1
            else:
                turtle.write('p', False, align="center", font=("Lucida Console", 20))
                index += 1
            cont = -80
            for letra in cadenaPila:
                turtle.penup(), turtle.setpos(-50, cont), turtle.pendown()
                turtle.write(letra, False, align="center", font=("Lucida Console", 20))
                cont -= 20
            sleep(1)

        # Finaliza la animación con el resultado
        turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()

        #dato = pila.quitar()  # Verifica si la pila está vacía al final
        ceros = cadenaMod.count('0')
        unos = cadenaMod.count('1')
        if ceros == unos:
            resultado += "(f, ε, Z)"
            turtle.clear()
            turtle.penup(), turtle.setpos(-53, 160), turtle.pendown()
            turtle.write('ε', False, align="left", font=("Lucida Console", 20))
            turtle.penup(), turtle.setpos(-50, 40), turtle.pendown()
            turtle.write('f', False, align="center", font=("Lucida Console", 20))
            cont = -80
            for letra in cadenaPila:
                turtle.penup(), turtle.setpos(-50, cont), turtle.pendown()
                turtle.write(letra, False, align="center", font=("Lucida Console", 20))
                cont -= 20
            sleep(1)

            turtle.penup(), turtle.setpos(-153, 200), turtle.pendown()
            turtle.write('Termina la animación', False, align="left", font=("Lucida Console", 20))

        else:  # Si la cadena no es aceptada
            if cadenaMod == "":
                resultado += "(f, ε, " + cadenaPila + ")\n"
            else:
                resultado += "(f, " + cadenaMod + ", " + cadenaPila + ")\n"
            turtle.penup(), turtle.setpos(-153, 200), turtle.pendown()
            turtle.write('La cadena no es aceptada', False, align="left", font=("Lucida Console", 20))

    # Escribe el resultado en un archivo de texto
    with open("Bloque_2\\Programa 4 autómata de pila\\automata_pila.txt", "w", encoding="utf-8") as f:
        f.write(resultado)


# Función principal que permite elegir la opción y manejar la entrada
def main():

    print("Seleccione una opción:")
    print("1. Ingresar la cadena manualmente")
    print("2. Generar una cadena automáticamente")

    opcion = int(input("Ingrese el número de su opción: "))

    if opcion == 1:
        cadena = input("Ingrese la cadena a evaluar (máximo 100,000 caracteres): ")
    elif opcion == 2:
        cadena = generarCadena()
        print(f"La cadena generada es: {cadena}")
    
    # Verifica que la longitud de la cadena esté dentro del límite
    if len(cadena) <= 100000:
        if len(cadena) <= 10:
            screen = Screen()  # Crea una pantalla para mostrar la animación
            animarAutomata(cadena=cadena)
            screen.mainloop()  # Ejecuta la animación de la pantalla
        else:
            print("La cadena supera los 10 caracteres. No se puede animar.")
    else:
        print("La cadena excede el límite máximo de caracteres (100,000).")


# Ejecuta la función principal
if __name__ == "__main__":
    main()
