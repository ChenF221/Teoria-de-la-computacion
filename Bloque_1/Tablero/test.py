import json

array = [1, 2, 3, 4, 5]

# Guardar array en archivo JSON
with open('archivo.json', 'w') as file:
    json.dump(array, file)
