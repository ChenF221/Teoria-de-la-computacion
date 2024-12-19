def buscador_palabra(word):
    """
    Verifica si la palabra termina en 'web' o 'ebay'.
    """
    # Definimos los estados como una tabla de transiciones.
    dfa = {
        'A': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'A'},
        'B': {'w': 'B', 'e': 'D', 'b': 'A', 'a': 'A', 'y': 'A'},
        'C': {'w': 'B', 'e': 'C', 'b': 'E', 'a': 'A', 'y': 'A'},
        'D': {'w': 'B', 'e': 'C', 'b': 'F', 'a': 'A', 'y': 'A'},
        'E': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'G', 'y': 'A'},
        'F': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'G', 'y': 'A'},
        'G': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'H'},
        'H': {'w': 'B', 'e': 'C', 'b': 'A', 'a': 'A', 'y': 'A'},
    }

    current_state = 'A'  # Estado inicial
    for char in word:  # Recorremos cada caracter
        if char in dfa[current_state]:
            current_state = dfa[current_state][char]  # Transición al siguiente estado
        else:
            current_state = 'A'  # Reiniciar si no coincide el caracter

    # Al final de la palabra, verificar si el estado actual es un estado final
    return current_state in {'F', 'H'}  # Estado 3 = 'web', Estado 7 = 'ebay'

# Pruebas
print(buscador_palabra("asdasdebay1")) 
print(buscador_palabra("thisisweb"))
print(buscador_palabra("testebay"))
print(buscador_palabra("webtest"))
print(buscador_palabra("testweb"))
print(buscador_palabra("ebay123"))
