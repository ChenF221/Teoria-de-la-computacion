def automata_buscador_palabra(word):
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

    current_state = '1'  # Estado inicial
    for char in word:
        current_state = transiciones[current_state].get(char, '1')

    # Estados finales
    final_states = {'22', '29', '38', '40', '43', '44', '45'}

    return current_state in final_states

# Pruebas
print(automata_buscador_palabra("acoso"))
print(automata_buscador_palabra("acecho"))
print(automata_buscador_palabra("agresión"))
print(automata_buscador_palabra("víctima"))
print(automata_buscador_palabra("violación"))
print(automata_buscador_palabra("violencia"))
print(automata_buscador_palabra("machista"))
print(automata_buscador_palabra("xdacosos"))




# import string

# # Abrir el archivo en modo lectura
# with open("Bloque_2\\Programa 3 Buscador de palabras\\texto.txt", "r") as archivo:
#     # Leer el contenido línea por línea
#     for linea in archivo:
#         # Eliminar los signos de puntuación de la línea
#         linea_sin_puntuacion = linea.translate(str.maketrans('', '', string.punctuation))
#         # Dividir la línea en palabras
#         palabras = linea_sin_puntuacion.split()
#         # Imprimir cada palabra
#         for palabra in palabras:
#             print(palabra, automata_buscador_palabra(palabra))


