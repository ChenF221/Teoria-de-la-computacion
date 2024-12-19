import random
import string
import turtle
import requests
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from time import sleep
from turtle import *


########################################## Programa 3 Buscador de palabras ##########################################################

def automata_buscador_palabra(word, historial, transiciones):

    estados_finales = {'22', '29', '38', '40', '43', '44', '45'}
    current_state = '1'

    for char in word:
        if char in transiciones[current_state]:
            next_state = transiciones[current_state][char]
        else:
            next_state = '1'
        historial.append((char, current_state, next_state))
        current_state = next_state

    return current_state in estados_finales


def procesar_contenido(contenido, salida_historial, transiciones):
    palabras_reservadas = {'acoso', 'acecho', 'agresión', 'víctima', 'violación', 'violencia', 'machista'}
    conteo_palabras = {palabra: [] for palabra in palabras_reservadas}

    with open(salida_historial, "w", encoding="utf-8") as historial_file:
        for x, linea in enumerate(contenido.splitlines(), start=1):
            linea_sin_puntuacion = linea.translate(str.maketrans('', '', string.punctuation))
            palabras = linea_sin_puntuacion.split()

            for y, palabra in enumerate(palabras, start=1):
                historial = []
                es_palabra_reservada = automata_buscador_palabra(palabra.lower(), historial, transiciones)

                historial_file.write(f"Palabra: {palabra}\n")
                for char, estado_actual, estado_siguiente in historial:
                    historial_file.write(f"  {char}: {estado_actual} -> {estado_siguiente}\n")
                historial_file.write("\n")

                if es_palabra_reservada and palabra.lower() in palabras_reservadas:
                    conteo_palabras[palabra.lower()].append((x, y))

    with open("Bloque_2\\programa3_resultado_palabras.txt", "w", encoding="utf-8") as resultado_file:
        for palabra, posiciones in conteo_palabras.items():
            resultado_file.write(f"{palabra}: {len(posiciones)} ocurrencias\n")
            for posicion in posiciones:
                resultado_file.write(f"  Linea {posicion[0]}, Palabra {posicion[1]}\n")


def obtener_texto_de_url(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error al obtener la URL: {e}")
        return ""


def grafica_dfa(transiciones, estados_finales):
    estados_finales_list = list(estados_finales)
    G = nx.DiGraph()

    for nodo in transiciones:
        G.add_node(nodo)


    # Agregar las transiciones como aristas y combinar etiquetas
    edge_labels_dict = {}  # Diccionario para agrupar etiquetas por aristas
    for nodo_actual, transiciones_letras in transiciones.items():
        for letra, nodo_destino in transiciones_letras.items():
            edge = (nodo_actual, nodo_destino)
            if edge not in edge_labels_dict:
                edge_labels_dict[edge] = []
            edge_labels_dict[edge].append(letra)
            

    for (nodo_origen, nodo_destino), letras in edge_labels_dict.items():
        G.add_edge(nodo_origen, nodo_destino, label=",".join(letras))


    node_colors = ['lightblue' if nodo not in estados_finales_list else 'lightgreen' for nodo in G.nodes()]

    pos = nx.spring_layout(G, seed=42)  # Posiciones para los nodos
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=12, font_weight="bold", arrows=True)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Mostrar el grafo
    plt.title("Grafo de Transiciones")
    plt.show()



def programa3():
    # alfabeto
    chars = ['a', 'c', 'o', 's', 'e', 'h', 'g', 'r', 'i', 'ó', 'n', 'v', 'í', 't', 'm', 'l']

    # todos los caracteres llevan a '1'
    def state_transitions(**overrides):
        base = {ch: '1' for ch in chars}
        base.update(overrides)
        return base

    transiciones = {
        '1': state_transitions(a='2', v='3', m='4'),
        '2': state_transitions(a='2', v='3', m='4', c='5', g='6'),
        '3': state_transitions(a='2', v='3', m='4', i='7', í='8'),
        '4': state_transitions(a='9', v='3', m='4'),
        '5': state_transitions(a='2', v='3', m='4', o='10', e='11'),
        '6': state_transitions(a='2', v='3', m='4', r='12'),
        '7': state_transitions(a='2', v='3', m='4', o='13'),
        '8': state_transitions(a='2', v='3', m='4', c='14'),
        '9': state_transitions(a='2', v='3', m='4', g='6', c='15'),
        '10': state_transitions(a='2', v='3', m='4', s='16'),
        '11': state_transitions(a='2', v='3', m='4', c='17'),
        '12': state_transitions(a='2', v='3', m='4', e='18'),
        '13': state_transitions(a='2', v='3', m='4', l='19'),
        '14': state_transitions(a='2', v='3', m='4', t='20'),
        '15': state_transitions(a='2', v='3', m='4', o='10', e='11', h='21'),
        '16': state_transitions(a='2', v='3', m='4', o='22'),
        '17': state_transitions(a='2', v='3', m='4', h='23'),
        '18': state_transitions(a='2', v='3', m='4', s='24'),
        '19': state_transitions(a='25', v='3', m='4', e='26'),
        '20': state_transitions(a='2', v='3', m='4', i='27'),
        '21': state_transitions(a='2', v='3', m='4', i='28'),
        '22': state_transitions(a='2', v='3', m='4'),
        '23': state_transitions(a='2', v='3', m='4', o='29'),
        '24': state_transitions(a='2', v='3', m='4', i='30'),
        '25': state_transitions(a='2', v='3', m='4', g='6', c='31'),
        '26': state_transitions(a='2', v='3', m='4', n='32'),
        '27': state_transitions(a='2', v='3', m='33'),
        '28': state_transitions(a='2', v='3', m='4', s='34'),
        '29': state_transitions(a='2', v='3', m='4'),
        '30': state_transitions(a='2', v='3', m='4', ó='35'),
        '31': state_transitions(a='2', v='3', m='4', o='10', e='11', i='36'),
        '32': state_transitions(a='2', v='3', m='4', c='37'),
        '33': state_transitions(a='38', v='3', m='4'),
        '34': state_transitions(a='2', v='3', m='4', t='39'),
        '35': state_transitions(a='2', v='3', m='4', n='40'),
        '36': state_transitions(a='2', v='3', m='4', ó='41'),
        '37': state_transitions(a='2', v='3', m='4', i='42'),
        '38': state_transitions(a='2', v='3', m='4', c='15', g='6'),
        '39': state_transitions(a='43', v='3', m='4'),
        '40': state_transitions(a='2', v='3', m='4'),
        '41': state_transitions(a='2', v='3', m='4', n='44'),
        '42': state_transitions(a='45', v='3', m='4'),
        '43': state_transitions(a='2', v='3', m='4', c='5', g='6'),
        '44': state_transitions(a='2', v='3', m='4'),
        '45': state_transitions(a='2', v='3', m='4', c='5', g='6'),
    }



    print("Seleccione la opción de entrada:")
    print("1. Leer desde un archivo de texto")
    print("2. Leer desde una página web")
    opcion = input("Ingrese el número de su elección: ")

    if opcion == "1":
        #ruta_archivo = input("Ingrese la ruta del archivo de texto: ")
        try:
            with open('Bloque_2\\Programa 3 Buscador de palabras\\texto.txt', "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
        except FileNotFoundError:
            print("Archivo no encontrado.")
            return
    elif opcion == "2":
        url = input("Ingrese la URL de la página web: ")
        contenido = obtener_texto_de_url(url)
        if not contenido:
            print("No se pudo obtener el contenido de la página web.")
            return
    else:
        print("Opción no válida.")
        return

    procesar_contenido(contenido, "Bloque_2\\programa3_historial_transiciones.txt", transiciones)

    estados_finales = {'22', '29', '38', '40', '43', '44', '45'}
    gra = input("¿Desea mostrar la grafica DFA? (s/n): ").strip().lower()
    if gra == 's':
        grafica_dfa(transiciones, estados_finales)




########################################## Programa 4 Automata de pila ###########################################################
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



def programa4():
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
        with open("Bloque_2\\programa4_resultado.txt", "w", encoding="utf-8") as f:
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





########################################## Programa 5 Backus-Naur Condicional IF #################################################
def derivar_gramatica(S, pasos):
    derivaciones = [f"Paso 1: {S}"]
    paso_actual = 2

    while pasos > 0:
        # Identificar las posibles opciones de reemplazo en S
        opciones = [simbolo for simbolo in ['S', 'A'] if simbolo in S]

        if not opciones:
            break  # Salir si no hay más símbolos para derivar

        # Elegir un símbolo al azar de las opciones disponibles
        eleccion = random.choice(opciones)

        if eleccion == 'A':
            if random.choice([True, False]): 
                S = S.replace('A', '(;eS)', 1)
                derivaciones.append(f"Paso {paso_actual}: Aplicamos A -> ;eS: {S}")
            else:  
                S = S.replace('A', '', 1)
                derivaciones.append(f"Paso {paso_actual}: Aplicamos A -> ε: {S}")
        elif eleccion == 'S':
            S = S.replace('S', '(iCtSA)', 1)  
            derivaciones.append(f"Paso {paso_actual}: Aplicamos S -> iCtSA: {S}")

        pasos -= 1
        paso_actual += 1

    return derivaciones

def convertir_a_pseudocodigo(expression):

    expression = expression[1:-1]  # Eliminar los paréntesis externos
    def parse_expression(expr, indent=0):
        result = ""

        while expr:
            char = expr[0]
            expr = expr[1:]

            if char == 'i':  # if
                result += " " * indent + "if (cond) then\n"
                result += " " * indent + "{\n"
                nested, expr = parse_expression(expr, indent + 4)
                result += nested
                result += " " * indent + "}\n"
            elif char == 'A':  # then
                pass
            elif char == 'S':  # statement
                result += " " * indent + "statement\n"
                break
            elif char == ';':  # else starts
                result += " " * indent + "else\n"
                result += " " * indent + "{\n"
                nested, expr = parse_expression(expr, indent + 4)
                result += nested
                result += " " * indent + "}\n"
            elif char == ')':  # end of a block
                indent -= 4
                break

        return result, expr

    pseudocode, _ = parse_expression(expression)
    return pseudocode


def programa5():
    max_derivaciones = 1000

    # Solicitar al usuario el modo de ejecución
    try:
        modo = int(input("Elige el modo de ejecución (1 para manual, 2 para automático): "))
    except ValueError:
        print("Entrada inválida. Se seleccionará el modo automático.")
        modo = 2

    # Determinar el número de derivaciones
    if modo == 1:
        try:
            num_derivaciones = int(input(f"Ingrese el número de derivaciones (hasta {max_derivaciones}): "))
            num_derivaciones = min(max_derivaciones, max(1, num_derivaciones))
        except ValueError:
            print("Entrada inválida. Se usará el número máximo de derivaciones.")
            num_derivaciones = max_derivaciones
    else:
        num_derivaciones = random.randint(1, max_derivaciones)

    # Derivaciones y generación de pseudo-código
    S = 'S'
    derivaciones = derivar_gramatica(S, num_derivaciones)

    with open('Bloque_2\\programa5_Derivaciones.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(derivaciones))

    if derivaciones:
        ultima_derivacion = derivaciones[-1].split(": ")[-1]
        pseudocodigo = convertir_a_pseudocodigo(ultima_derivacion)
        with open('Bloque_2\\programa5_Pseudocodigo.txt', 'w', encoding='utf-8') as f:
            f.write(pseudocodigo)

    print("Las derivaciones se han guardado en 'Derivaciones.txt'")
    print("El pseudo-código se ha guardado en 'Pseudocodigo.txt'")





########################################## Programa 6 Máquina de Turing ##########################################################
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
                        screen.bye()
                    return resultado


def generarCadena(max_length=1000):
    asignacion = random.randint(1, max_length)
    cadena = ""
    if asignacion > 0:
        cadena += str(0) * asignacion  # Agregar ceros
        cadena += str(1) * asignacion  # Agregar unos
    return cadena



def programa6():
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

    

    resultado = tm.ejecutar_con_animacion(archivo_salida="Bloque_2\\programa6_salidaTM.txt", mostrar_animacion=mostrar_animacion)
    if resultado:
        print(f"\nLa cadena {cadena} ES aceptada. Los pasos se ha guardado en 'salidaTM.txt'.\n")
    else:
        print(f"\nLa cadena {cadena} NO es aceptada. Los pasos se ha guardado en 'salidaTM.txt'.\n")




#################### MENU PRINCIPAL ####################

def mostrar_menu():
    print("\n================== MENU ==================")
    print("Selecciona un programa para ejecutar:")
    print("1. Programa Buscador de palabras")
    print("2. Programa Automata de pila")
    print("3. Programa Backus-Naur Condicional IF")
    print("4. Programa Máquina de Turing")
    print("5. Salir")
    print("==========================================\n")


def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            programa3()
        elif opcion == "2":
            programa4()
        elif opcion == "3":
            programa5()
        elif opcion == "4":
            programa6()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()