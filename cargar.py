import json
import mysql.connector

# === CONFIGURACIÓN DE CONEXIÓN A LA DB ===
conexion = mysql.connector.connect(
    host="sql5.freesqldatabase.com",
    user="sql5807118",
    password="KlPzLnH7ca",
    database="sql5807118"
)
cursor = conexion.cursor()

# Cargar archivo JSON
with open("enfermedades_limpio.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Insertar diagnósticos y síntomas
for item in datos:
    nombre_diag = item["nombre"]

    # Insertar diagnóstico si no existe
    cursor.execute("SELECT id_diagnostico FROM diagnosticos WHERE nombre = %s", (nombre_diag,))
    resultado_diag = cursor.fetchone()

    if resultado_diag:
        id_diagnostico = resultado_diag[0]
    else:
        cursor.execute("INSERT INTO diagnosticos (nombre, descripcion) VALUES (%s, %s)", (nombre_diag, ""))
        conexion.commit()
        id_diagnostico = cursor.lastrowid
        print(f"✅ Diagnóstico insertado: {nombre_diag}")

    # Insertar síntomas asociados
    for sintoma_nombre in item["sintomas"]:
        cursor.execute("SELECT id_sintoma FROM sintomas WHERE nombre = %s", (sintoma_nombre,))
        resultado_sintoma = cursor.fetchone()

        if not resultado_sintoma:
            cursor.execute("INSERT INTO sintomas (nombre, descripcion) VALUES (%s, %s)", (sintoma_nombre, ""))
            conexion.commit()
            print(f"   🩺 Síntoma insertado: {sintoma_nombre}")
        else:
            print(f"   ⚠️ Síntoma ya existe: {sintoma_nombre}")

print("\n🚀 Carga completada correctamente.")
cursor.close()
conexion.close()