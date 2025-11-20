import os
from google.cloud import bigquery

# Configurá la ruta de las credenciales y la carpeta con los CSV
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\maria\proyecto-analisis-adicciones-6db22eb015db.json"
CARPETA_CSV = r"C:\Users\maria\OneDrive\Escritorio\backups...secretaria\csvs"

# Parámetros de BigQuery
ID_PROYECTO = "proyecto-analisis-adicciones"        # Cambialo por tu proyecto de GCP
DATASET = "backups_cas_2023_07"                   # Dataset creado en BigQuery

client = bigquery.Client(project=ID_PROYECTO)

def subir_csv_a_bigquery(ruta_csv, tabla):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,     # Saltar header
        autodetect=True,         # Auto detectar esquema
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Sobrescribir tabla si existe
    )

    with open(ruta_csv, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            f"{ID_PROYECTO}.{DATASET}.{tabla}",
            job_config=job_config
        )
    job.result()  # Esperar a que termine el job
    print(f"✅ Archivo '{os.path.basename(ruta_csv)}' cargado en {tabla}.")

def main():
    archivos = [f for f in os.listdir(CARPETA_CSV) if f.endswith(".csv")]
    for archivo in archivos:
        nombre_tabla = os.path.splitext(archivo)[0].replace("-", "_").replace(" ", "_").lower()
        ruta_archivo = os.path.join(CARPETA_CSV, archivo)
        try:
            subir_csv_a_bigquery(ruta_archivo, nombre_tabla)
        except Exception as e:
            print(f"❌ Error cargando {archivo}: {e}")

if __name__ == "__main__":
    main()
