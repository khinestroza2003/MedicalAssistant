import json

# Cargar el archivo JSON
with open('enfermedades_optimizado.json', 'r') as file:
    data = json.load(file)

# Crear una lista para almacenar los datos limpios
resultado = []

# Procesar cada enfermedad
for item in data:
    if 'nombre' in item and 'sintomas' in item:
        # Filtrar solo los síntomas que contienen ":"
        sintomas_limpios = [sintoma.split(":")[0] for sintoma in item['sintomas'] if ":" in sintoma]
        resultado.append({
            'nombre': item['nombre'],
            'sintomas': sintomas_limpios
        })

# Guardar el nuevo JSON limpio
with open('enfermedades_limpio.json', 'w') as file:
    json.dump(resultado, file, indent=4, ensure_ascii=False)

print("Archivo JSON limpio generado como 'enfermedades_limpio.json'")