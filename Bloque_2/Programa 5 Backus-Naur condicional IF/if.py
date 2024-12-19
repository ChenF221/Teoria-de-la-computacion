import random

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


def main():
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

    with open('Bloque_2\\Programa 5 Backus-Naur condicional IF\\Programa_5_Derivaciones.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(derivaciones))

    if derivaciones:
        ultima_derivacion = derivaciones[-1].split(": ")[-1]
        pseudocodigo = convertir_a_pseudocodigo(ultima_derivacion)
        with open('Bloque_2\\Programa 5 Backus-Naur condicional IF\\Programa_5_Pseudocodigo.txt', 'w', encoding='utf-8') as f:
            f.write(pseudocodigo)

    print("Las derivaciones se han guardado en 'Derivaciones.txt'")
    print("El pseudo-código se ha guardado en 'Pseudocodigo.txt'")


if __name__ == "__main__":
    main()
