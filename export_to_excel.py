import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Configurar conexión a MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "login_db")
)

def exportar_usuarios_a_excel():
    """Exporta la tabla users_new a un archivo Excel"""
    try:
        # Leer datos de la base de datos
        query = "SELECT * FROM users_new"
        df = pd.read_sql(query, db)
        
        # Crear nombre del archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_usuarios_{timestamp}.xlsx"

        # Guardar en la carpeta Descargas del usuario
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(downloads_dir, exist_ok=True)
        file_path = os.path.join(downloads_dir, filename)
        
        # Guardar a Excel
        df.to_excel(file_path, index=False, sheet_name="Usuarios")
        
        print(f"✅ Exportación exitosa: {file_path}")
        print(f"📊 Total de registros: {len(df)}")
        print(f"📋 Columnas: {', '.join(df.columns.tolist())}")
        
        return filename
    
    except Exception as e:
        print(f"❌ Error en la exportación: {e}")
        return None
    
    finally:
        db.close()

if __name__ == "__main__":
    exportar_usuarios_a_excel()
