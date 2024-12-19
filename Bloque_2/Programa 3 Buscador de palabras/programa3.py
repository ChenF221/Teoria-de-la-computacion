import string
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt


def automata_buscador_palabra(word, historial, transiciones):

    estados_finales = {'22', '29', '38', '40', '43', '44', '45'}
    current_state = '1'

    for char in word:
        next_state = transiciones[current_state].get(char, '1')
        historial.append((char, current_state, next_state))
        current_state = next_state

    return current_state in estados_finales


def procesar_contenido(contenido, salida_historial, transiciones):
    palabras_reservadas = {'escuela', 'estudiantes', 'rencor', 'rifles', 'crimen', 'armas'}
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

    with open("Bloque_2\\Programa 3 Buscador de palabras\\resultado_palabras.txt", "w", encoding="utf-8") as resultado_file:
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



def main():


    # alfabeto
    chars = ['a', 'c', 'o', 's', 'e', 'h', 'g', 'r', 'i', 'ó', 'n', 'v', 'í', 't', 'm', 'l']

    # Función auxiliar para crear un diccionario de transiciones por estado.
    # Por defecto, todos los caracteres llevan a '1' a menos que se especifique lo contrario.
    def state_transitions(**overrides):
        # Retorna un diccionario donde cada carácter en chars mapea a '1', 
        # y si está en overrides, se usa el valor dado en overrides.
        base = {ch: '1' for ch in chars}
        base.update(overrides)
        return base

    # Definimos los estados usando la función auxiliar, sólo listando las excepciones:
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
        '45': state_transitions(a='2', v='3', m='4', c='5'),
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

    procesar_contenido(contenido, "Bloque_2\\Programa 3 Buscador de palabras\\historial_transiciones.txt", transiciones)

    estados_finales = {'26', '31', '32', '33', '35', '39'}
    gra = input("¿Desea mostrar la animación? (s/n): ").strip().lower()
    if gra == 's':
        grafica_dfa(transiciones, estados_finales)

if __name__ == "__main__":
    main()
