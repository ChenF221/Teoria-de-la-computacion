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
                #indent -= 4
                break

        return result, expr

    pseudocode, _ = parse_expression(expression)
    return pseudocode

# Ejemplo:
expression = "(iCt(iCt(iCt(iCt(iCtS)A))(;eS))(;eS))"
print(convertir_a_pseudocodigo(expression))

