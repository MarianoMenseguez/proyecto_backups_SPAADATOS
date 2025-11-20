import re
import csv
import os

def procesar_copy(contenido):
    patron_copy = re.compile(r"COPY\s+(\w+)\s+\((.*?)\)\s+FROM stdin;\s*(.*?)(?=\\\.)", re.DOTALL)
    matches = patron_copy.finditer(contenido)

    for match in matches:
        tabla = match.group(1)
        columnas = [col.strip() for col in match.group(2).split(",")]
        datos_raw = match.group(3).strip().split("\n")

        filas = [linea.split("\t") for linea in datos_raw]

        archivo_csv = f"{tabla}.csv"
        with open(archivo_csv, "w", newline='', encoding="utf-8") as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(columnas)
            writer.writerows(filas)

        print(f"✅ Exportado: {archivo_csv}")

# Procesar todos los .sql del directorio
for archivo_sql in os.listdir():
    if archivo_sql.endswith(".sql"):
        print(f"🔄 Procesando {archivo_sql}...")
        with open(archivo_sql, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
            procesar_copy(contenido)
