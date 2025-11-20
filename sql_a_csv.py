import re
import csv
import os

# Regex para capturar sentencias INSERT INTO
patron_insert = re.compile(
    r"INSERT INTO\s+\"?(?P<tabla>\w+)\"?\s*\((?P<columnas>.*?)\)\s+VALUES\s+(?P<valores>.+?);",
    re.DOTALL | re.IGNORECASE,
)

# Función para limpiar y dividir valores
def procesar_valores(valores_str):
    registros = re.findall(r"\((.*?)\)", valores_str)
    datos = []
    for registro in registros:
        campos = [campo.strip().strip("'") for campo in registro.split(",")]
        datos.append(campos)
    return datos

# Buscar todos los archivos .sql en la carpeta actual
for archivo_sql in os.listdir():
    if archivo_sql.endswith(".sql"):
        print(f"🔄 Procesando {archivo_sql}...")
        with open(archivo_sql, "r", encoding="utf-8") as f:
            contenido = f.read()

        tablas_encontradas = 0

        for match in patron_insert.finditer(contenido):
            tabla = match.group("tabla")
            columnas = [col.strip().strip('"') for col in match.group("columnas").split(",")]
            valores = procesar_valores(match.group("valores"))

            nombre_archivo = f"{tabla}.csv"
            with open(nombre_archivo, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columnas)
                writer.writerows(valores)

            print(f"✅ Exportado: {nombre_archivo}")
            tablas_encontradas += 1

        if tablas_encontradas == 0:
            print(f"⚠️  No se encontraron INSERTs válidos en {archivo_sql}")

