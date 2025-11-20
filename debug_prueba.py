import os
from google.cloud import bigquery

# 🔧 Establecer manualmente la ruta del JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\maria\proyecto-analisis-adicciones-6db22eb015db.json"

print("🔍 Variable GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# ✅ Intentar conectar a BigQuery
try:
    client = bigquery.Client()
    print("✅ Conectado correctamente al proyecto:", client.project)
except Exception as e:
    print("❌ Error al conectarse a BigQuery:")
    print(e)
