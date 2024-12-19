import random
import turtle
from time import sleep

class PushdownAutomaton:
    def __init__(self, Q, Σ, Γ, δ, q0, Z0, F):
        self.Q = Q
        self.Sigma = Σ
        self.Gamma = Γ
        self.delta = δ
        self.q0 = q0
        self.Z0 = Z0
        self.F = F

    def _transitions(self, q, a, X):
        if (q, a, X) in self.delta:
            return self.delta[(q, a, X)]
        return []

    def simulate(self, w):
        stack = [(self.q0, 0, [self.Z0], [])]
        visited = set()
        last_dead_end_path = None

        w_len = sum(1 for _ in w)

        while stack:
            q, i, pila, path = stack.pop()
            # Convertimos pila a string
            stack_str = "".join(pila)
            # w_restante es w[i:] si i < w_len, sino "ε"
            w_restante = w[i:] if i < w_len else "ε"

            current_config = (q, w_restante, stack_str)
            current_path = path + [current_config]

            # Checar aceptación (i == w_len)
            if i == w_len and q in self.F:
                return True, current_path

            conf_signature = (q, i, tuple(pila))
            if conf_signature in visited:
                continue
            visited.add(conf_signature)

            did_move = False
            a = w[i] if i < w_len else None

            # Transiciones consumiendo entrada
            if a is not None and pila:
                X = pila[0]
                for (q_next, to_push) in self._transitions(q, a, X):
                    did_move = True
                    new_stack = pila[1:]
                    if to_push != "ε":
                        # Insertar símbolos en orden inverso
                        for sym in reversed(to_push):
                            new_stack.insert(0, sym)
                    stack.append((q_next, i+1, new_stack, current_path))

            # Transiciones epsilon
            if pila:
                X = pila[0]
                for (q_next, to_push) in self._transitions(q, "ε", X):
                    did_move = True
                    new_stack = pila[1:]
                    if to_push != "ε":
                        for sym in reversed(to_push):
                            new_stack.insert(0, sym)
                    stack.append((q_next, i, new_stack, current_path))

            if not did_move:
                last_dead_end_path = current_path

        return False, last_dead_end_path


def animarAutomata(path, accepted):
    screen = turtle.Screen()
    screen.title("Animación PDA")
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # Dibujar marco
    t.penup()
    t.goto(-100, 100)
    t.pendown()
    t.color("black")
    t.begin_fill()
    fill_colors = ["yellow", "green"]
    for lado in range(4):
        t.fillcolor(fill_colors[lado % 2])
        t.forward(100)
        t.right(90)
    t.end_fill()

    # Flechas
    t.penup()
    t.goto(-50, 100)
    t.pendown()
    t.goto(-50, 150)
    t.goto(-45, 140)
    t.goto(-50, 150)
    t.goto(-55, 140)

    t.penup()
    t.goto(-50, 0)
    t.pendown()
    t.goto(-50, -50)
    t.goto(-45, -40)
    t.goto(-50, -50)
    t.goto(-55, -40)

    writer = turtle.Turtle()
    writer.hideturtle()
    writer.speed(0)

    path_length = sum(1 for _ in path)

    # Iterar sobre configuraciones
    index_gen = (i for i in range(path_length))  # Generador para indices
    for i in index_gen:
        q, w_rest, stack_str = path[i]
        writer.clear()
        writer.penup()
        writer.goto(-53, 160)
        writer.pendown()

        # Si w_rest == "" -> "ε"
        w_rest_len = sum(1 for _ in w_rest)
        if w_rest_len == 0:
            w_rest = "ε"

        writer.write(w_rest, False, align="left", font=("Arial", 20))

        # Estado
        writer.penup()
        writer.goto(-50, 40)
        writer.pendown()
        writer.write(q, False, align="center", font=("Arial", 20))

        # Pila
        cont = -80
        for letra in stack_str:
            writer.penup()
            writer.goto(-50, cont)
            writer.pendown()
            writer.write(letra, False, align="center", font=("Arial", 20))
            cont -= 20

        sleep(1)

    # Mensaje final
    writer.penup()
    writer.goto(-153, 200)
    writer.pendown()
    if accepted:
        writer.write('La cadena es aceptada', False, align="left", font=("Arial", 20))
    else:
        writer.write('La cadena no es aceptada', False, align="left", font=("Arial", 20))

    screen.mainloop()


def generarCadena(max_length=100000):
    asignacion = random.randint(1, max_length)
    cadena = ""
    if asignacion > 0:
        cadena += str(0) * asignacion  # Agregar ceros
        cadena += str(1) * asignacion  # Agregar unos
    return cadena



def main():
    Q = {"q", "p", "f"}
    Σ = {"0", "1"}
    Γ = {"Z", "X"}
    q0 = "q"
    Z0 = "Z"
    F = {"f"}

    δ = {
        ("q", "0", "Z"): [("q", "XZ")],
        ("q", "0", "X"): [("q", "XX")],
        ("q", "1", "X"): [("p", "ε")],
        ("p", "1", "X"): [("p", "ε")],
        ("p", "ε", "Z"): [("f", "Z")]
    }

    pda = PushdownAutomaton(Q, Σ, Γ, δ, q0, Z0, F)

    print("Seleccione una opción:")
    print("1. Ingresar la cadena manualmente")
    print("2. Generar una cadena automáticamente")

    opcion = int(input("Ingrese el número de su opción: "))

    if opcion == 1:
        w = input("Ingrese la cadena a evaluar (máximo 100,000 caracteres): ")
    elif opcion == 2:
        w = generarCadena()
        print(f"La cadena generada es: {w}")
    else:
        print("Opción no válida.")
        return

    # Simular el PDA
    accepted, path = pda.simulate(w)

    # Guardar el resultado en resultado.txt
    if path is not None:
        path_length = sum(1 for _ in path)
        with open("Bloque_2\\Programa 4 autómata de pila\\resultado.txt", "w", encoding="utf-8") as f:
            path_list = [c for c in path]
            for i in range(path_length):
                q, w_rest, st = path_list[i]
                if sum(1 for _ in w_rest) == 0:
                    w_rest = "ε"
                # si es la última y aceptada, sin ⊦
                if accepted and i == (path_length - 1):
                    f.write(f"({q}, {w_rest}, {st})\n")
                else:
                    if i < (path_length - 1):
                        f.write(f"({q}, {w_rest}, {st})⊦\n")
                    else:
                        f.write(f"({q}, {w_rest}, {st})\n")
        print("Procedimiento guardado en resultado.txt")
    else:
        print("No se generaron configuraciones (path es None).")

    if accepted:
        print(f"La cadena {w} es aceptada por el PDA.")
    else:
        print(f"La cadena {w} NO es aceptada por el PDA.")

    # Si la longitud de la cadena es <= 10, preguntar si se desea mostrar la animación
    w_length = sum(1 for _ in w)
    if w_length <= 10 and path is not None:
        opcion_animacion = input("¿Desea mostrar la animación? (s/n): ").strip().lower()
        if opcion_animacion == 's':
            animarAutomata(path, accepted)
        else:
            print("Animación omitida.")
    elif w_length > 10:
        print("La cadena supera los 10 caracteres. No se mostrará la animación.")


if __name__ == "__main__":
    main()
