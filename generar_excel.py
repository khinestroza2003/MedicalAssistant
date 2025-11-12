import json
import openpyxl

# Cargar el archivo JSON
with open('enfermedades_optimizado.json', 'r') as file:
    data = json.load(file)

# Crear un nuevo libro de Excel
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Enfermedades y Síntomas"

# Escribir encabezados
sheet.append(["Nombre de la Enfermedad", "Síntomas"])

# Escribir los datos en el archivo Excel
for item in data:
    nombre = item.get('nombre', "")
    sintomas = ", ".join(item.get('sintomas', []))
    sheet.append([nombre, sintomas])

# Guardar el archivo Excel
workbook.save("enfermedades_optimizado.xlsx")

print("Archivo Excel generado como 'enfermedades_optimizado.xlsx'")