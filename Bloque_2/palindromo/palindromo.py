import random

def generate_P():
    # Elegir aleatoriamente una de las reglas de producción
    rule = random.choice([1, 2, 3, 4, 5])

    if rule == 1:
        print("Regla 1: P -> ε")
        return "ε"  # Regla 1: P -> ε
    elif rule == 2:
        print("Regla 2: P -> 0")
        return "0"  # Regla 2: P -> 0
    elif rule == 3:
        print("Regla 3: P -> 1")
        return "1"  # Regla 3: P -> 1
    elif rule == 4:
        print("Regla 4: P -> 0P0")
        return "0" + generate_P() + "0"  # Regla 4: P -> 0P0
    elif rule == 5:
        print("Regla 5: P -> 1P1")
        return "1" + generate_P() + "1"  # Regla 5: P -> 1P1

# Generar una cadena a partir de la gramática
result = generate_P()
print("Cadena generada:", result)
