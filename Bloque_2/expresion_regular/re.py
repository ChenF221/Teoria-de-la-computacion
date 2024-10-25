import random

"""
(0 + 10)*(ε + 1)
Expresion regular de las cadenas 0's y 1's sin tener dos 1's seguidos.
"""

def generar_cadena_aleatoria(longitud_maxima=10):
    partes = []
    
    for _ in range(random.randint(0, longitud_maxima // 2)):
        if random.choice([True, False]):
            partes.append('0')
        else:
            partes.append('10')
    
    # Definir parte_1 y parte_2
    parte_1 = ''.join(partes)
    parte_2 = ''

    if random.choice([True, False]):
        parte_2 = '1'
    
    partes_finales = [parte_1, parte_2]
    random.shuffle(partes_finales)

    cadena_aleatoria = ''.join(partes_finales)
    return cadena_aleatoria

def validar_cadena(cadena):
    # Si la cadena cumple con la estructura (0 + 10)*(ε + 1)
    
    # Etapa 1: Verificar patrones (0 + 10)*
    i = 0
    contador = 0  # Contador para la longitud de la cadena
    for char in cadena:
        contador += 1  # Incrementar el contador en cada iteración

    while i < contador:
        if cadena[i] == '0':
            i += 1  # Pasar '0'
        elif i + 1 < contador and cadena[i] == '1' and cadena[i + 1] == '0':
            i += 2  # Pasar '10'
        else:
            break  # Salir si no hay '0' o '10'
    
    # Etapa 2: Verificar que termine en ε o '1'
    return i == contador or (i == contador - 1 and cadena[i] == '1')

def main():
    for i in range(10):
        cadena = generar_cadena_aleatoria(longitud_maxima=100)
        
        # Validar la cadena generada
        if validar_cadena(cadena):
            print(f"Cadena {i}: '{cadena}' cumple.")
        else:
            print(f"Cadena {i}: '{cadena}' NO cumple.")

if __name__ == "__main__":
    main()
