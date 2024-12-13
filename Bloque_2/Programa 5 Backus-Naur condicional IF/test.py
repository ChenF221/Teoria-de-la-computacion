def generate_pseudocode(expression):

    expression = expression[1:-1]  # Eliminar los paréntesis externos
    def parse_expression(expr, indent=0):
        result = ""
        count = 0
        while expr:
            char = expr[0]
            expr = expr[1:]

            if char == '(':
                count += 1

            if char == 'i':  # if
                result += " " * indent + "if (cond) then\n"
                result += " " * indent + "{\n"
                nested, expr = parse_expression(expr, indent + 4)
                result += nested
                result += " " * indent + "}\n"
            elif char == 'A':  # then
                break
            elif char == 'S':  # statement
                result += " " * indent + "statement\n"
            elif char == ';':  # else starts
                result += " " * indent + "else\n"
                result += " " * indent + "{\n"
                nested, expr = parse_expression(expr, indent + 4)
                result += nested
                result += " " * indent + "}\n"
            elif char == ')':  # end of a block
                count -= 1
                break

        return result, expr

    pseudocode, _ = parse_expression(expression)
    return pseudocode

# Guardar el resultado en un archivo txt
def save_to_txt(expression, filename):
    pseudocode = generate_pseudocode(expression)
    with open(filename, 'w') as file:
        file.write(pseudocode)

# Ejecutar y guardar el resultado
expression = "iCt(iCt(iCt(iCtSA)A)(;eS))A"
save_to_txt(expression, "pseudocode.txt") 
