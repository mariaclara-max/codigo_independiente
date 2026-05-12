import pandas as pd
from datetime import datetime
from pathlib import Path

# =========================================================
# CONFIGURACIÓN DE RUTAS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent

# Carpeta de salida para los resultados finales (Solo Emails)
OUTPUT_DIR = BASE_DIR / 'Bounces_rejected_Resultados'
OUTPUT_DIR.mkdir(exist_ok=True)

# Archivo histórico para evitar procesar dos veces lo mismo
HISTORY_FILE = BASE_DIR / 'archivos_ya_leidos.txt'

# Parámetros de filtrado
DOMINIO = '@email.it'
MENSAJE_BUSCADO = 'Recipient address rejected: This mailbox does not exist or has been closed down'
TAMANO_BLOQUE = 150000  # Aumentamos un poco el bloque para mayor velocidad

# =========================================================
# LOGICA DE PROCESAMIENTO
# =========================================================

def obtener_historial():
    if not HISTORY_FILE.exists():
        return set()
    return set(HISTORY_FILE.read_text().splitlines())

def guardar_en_historial(nombre_archivo):
    with open(HISTORY_FILE, 'a') as f:
        f.write(f"{nombre_archivo}\n")

def filtrar_bounce_gigante(ruta_csv):
    fecha_hoy = datetime.now().strftime('%Y_%m_%d')
    # Nombre descriptivo para el archivo de salida
    archivo_salida = OUTPUT_DIR / f'Emails_Rechazados_{fecha_hoy}.csv'
    
    print(f"[*] Analizando: {ruta_csv.name}...")
    
    # Variable para controlar la creación del archivo y su cabecera
    es_primera_escritura = not archivo_salida.exists()

    try:
        # Leemos el archivo gigante por trozos
        reader = pd.read_csv(ruta_csv, chunksize=TAMANO_BLOQUE, low_memory=False)
        
        total_encontrados = 0

        for i, chunk in enumerate(reader):
            # 1. Limpieza de nombres de columnas
            chunk.columns = chunk.columns.str.strip()
            
            # 2. Definir filtros
            # Filtro 1: El mensaje de error específico
            mask_msg = chunk['Message'].str.contains(MENSAJE_BUSCADO, case=False, na=False)
            # Filtro 2: El dominio del correo
            mask_dom = chunk['Email'].str.endswith(DOMINIO, na=False)
            
            # 3. Aplicar filtros y SELECCIONAR SOLO LA COLUMNA EMAIL
            # Aquí ocurre la optimización: descartamos 'Message' y otras columnas de inmediato
            df_filtrado = chunk.loc[mask_msg & mask_dom, ['Email']]

            # 4. Guardado incremental (Append)
            if not df_filtrado.empty:
                total_encontrados += len(df_filtrado)
                
                # 'w' si es el primer bloque del día, 'a' (append) para los siguientes
                modo = 'w' if es_primera_escritura else 'a'
                incluir_cabecera = es_primera_escritura
                
                df_filtrado.to_csv(archivo_salida, mode=modo, index=False, header=incluir_cabecera)
                es_primera_escritura = False 

            if (i + 1) % 10 == 0:
                print(f"    -> {((i + 1) * TAMANO_BLOQUE) / 1_000_000:.1f} Millones de filas revisadas...")

        print(f"    [+] Se encontraron {total_encontrados} registros válidos.")
        return True
    except Exception as e:
        print(f"    [!] Error crítico en {ruta_csv.name}: {e}")
        return False

# =========================================================
# EJECUCIÓN
# =========================================================

def main():
    ya_procesados = obtener_historial()
    
    # Busca archivos que cumplan el patrón en la carpeta actual
    archivos_nuevos = [
        f for f in BASE_DIR.glob('bounce-stats-*.csv') 
        if f.name not in ya_procesados
    ]

    if not archivos_nuevos:
        print("[.] No se han detectado archivos nuevos para procesar.")
        return

    print(f"[+] Archivos nuevos detectados: {len(archivos_nuevos)}")

    for archivo in archivos_nuevos:
        if filtrar_bounce_gigante(archivo):
            guardar_en_historial(archivo.name)
            print(f"[OK] {archivo.name} procesado correctamente.\n")

if __name__ == "__main__":
    main()