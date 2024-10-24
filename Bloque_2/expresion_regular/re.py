import random

def generar_cadena_aleatoria(longitud_maxima=10):
    # Generar la primera parte: '1*', una secuencia de 0 a n unos.
    parte_1 = '1' * random.randint(0, longitud_maxima)

    # Generar la parte obligatoria: exactamente un '0'.
    parte_2 = '0'

    # Generar la tercera parte: '(0+1)*', una secuencia de 0 a n caracteres '0' o '1'.
    parte_3 = ''.join(random.choice('01') for _ in range(random.randint(0, longitud_maxima)))

    # Combinar las partes
    cadena_aleatoria = parte_1 + parte_2 + parte_3
    return cadena_aleatoria

def validar_cadena(cadena):
    # si la cadena cumple con la estructura '1*0(0+1)*'
    
    # Etapa 1: Verificar la parte inicial '1*'
    i = 0
    while i < len(cadena) and cadena[i] == '1':
        i += 1

    # Etapa 2: Verificar si hay al menos un '0' después de los '1'
    if i >= len(cadena) or cadena[i] != '0':
        return False

    # Pasar el '0'
    i += 1

    # Etapa 3: Verificar la parte '(0+1)*'
    while i < len(cadena):
        if cadena[i] not in ('0', '1'):
            return False
        i += 1

    # Si hemos llegado hasta aquí, la cadena cumple con la expresión regular
    return True

for i in range(10):
    cadena = generar_cadena_aleatoria(longitud_maxima=10)
    #print(f"Cadena {i}:", cadena)

    # Validar la cadena generada
    if validar_cadena(cadena):
        print(f"Cadena {i}:", cadena + " cumple.")
    else:
        print(f"Cadena {i}:", cadena + " NO cumple.")