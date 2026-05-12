from pathlib import Path
import pandas as pd

# =========================================================
# CONFIGURACIÓN DE RUTAS (Ajustado a tu ubicación real)
# =========================================================

# El script detecta que los archivos están en la misma carpeta que él
BASE_DIR = Path(__file__).resolve().parent

# Carpeta final para los bloques de 2,000
final_output_dir = BASE_DIR / 'EMAIL_FINAL_RECORD'
final_output_dir.mkdir(exist_ok=True)

rows_per_new_file = 2000

# =========================================================
# PROCESAMIENTO
# =========================================================

def unificar_directorio_actual():
    try:
        print(f"[*] Buscando archivos CSV en: {BASE_DIR}")
        
        # 1. BUSCAR ARCHIVOS .CSV EN LA CARPETA ACTUAL
        # Evitamos leer los que ya están en la carpeta de salida
        archivos_csv = [
            f for f in BASE_DIR.glob('*.csv') 
            if 'Email_Final' not in f.name and f.name != 'Hards_to_Promo.csv'
        ]
        
        if not archivos_csv:
            print("[-] No se encontraron archivos CSV procesables en esta carpeta.")
            return

        print(f"[*] Se han encontrado {len(archivos_csv)} archivos.")
        
        lista_emails = []

        # 2. PROCESAR CADA ARCHIVO
        for archivo in archivos_csv:
            print(f"    -> Procesando: {archivo.name}")
            
            # Leemos el archivo
            df_temp = pd.read_csv(archivo)
            
            # Limpieza de nombres de columnas
            df_temp.columns = df_temp.columns.str.strip()
            
            # Buscamos la columna Email (sin importar mayúsculas)
            col_email = next((c for c in df_temp.columns if c.lower() == 'email'), None)
            
            if col_email:
                # Extraemos y limpiamos nulos
                emails = df_temp[[col_email]].dropna()
                emails.columns = ['Email'] # Estandarizamos el nombre
                lista_emails.append(emails)
            else:
                print(f"    [!] Advertencia: No se halló columna 'Email' en {archivo.name}")

        if not lista_emails:
            print("[-] No se pudo extraer ningún email de los archivos encontrados.")
            return

        # 3. UNIFICAR
        df_unificado = pd.concat(lista_emails, ignore_index=True)
        total = len(df_unificado)
        print(f"\n[*] TOTAL DE EMAILS UNIFICADOS: {total}")

        # 4. DIVIDIR EN BLOQUES DE 2,000
        print(f"[*] Creando archivos de {rows_per_new_file} registros...")
        
        count = 0
        for i in range(0, total, rows_per_new_file):
            count += 1
            chunk = df_unificado.iloc[i : i + rows_per_new_file]
            
            nombre_salida = f'Email_Final_Parte_{count}.csv'
            chunk.to_csv(final_output_dir / nombre_salida, index=False)

        print(f"\n[OK] Proceso terminado con éxito.")
        print(f"[OK] Los {count} archivos están en: {final_output_dir}")

    except Exception as e:
        print(f"[-] Error inesperado: {e}")

if __name__ == "__main__":
    unificar_directorio_actual()