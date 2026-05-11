from pathlib import Path
import pandas as pd

# =========================================================
# CONFIGURACIÓN:Dividir las listas de correo electrónico en partes más pequeñas 10,000 filas por archivo
# =========================================================

# Carpeta donde está el script actual
BASE_DIR = Path(__file__).resolve().parent

# Nombre del archivo CSV original
file_path = BASE_DIR / 'Hards_to_Promo.csv'

# Número de filas por archivo
rows_per_file = 10000


# Carpeta de salida
output_dir = BASE_DIR / 'output_parts'

# Crear carpeta si no existe
output_dir.mkdir(exist_ok=True)

# =========================================================
# PROCESAMIENTO
# =========================================================

try:
    print(f'Buscando archivo en: {file_path}')

    # Leer y dividir el CSV por bloques
    for i, chunk in enumerate(
        pd.read_csv(file_path, chunksize=rows_per_file)
    ):
        # Nombre del archivo de salida
        output_file = output_dir / f'Hards_to_Promo_{i + 1}.csv'

        # Guardar chunk
        chunk.to_csv(output_file, index=False)

        print(f'Archivo generado: {output_file}')

    print(
        f'\nDivisión completada correctamente '
        f'en bloques de {rows_per_file} filas.'
    )

# =========================================================
# MANEJO DE ERRORES
# =========================================================

except FileNotFoundError:
    print('\nERROR: El archivo CSV no existe.')

except pd.errors.EmptyDataError:
    print('\nERROR: El archivo CSV está vacío.')

except pd.errors.ParserError:
    print('\nERROR: El archivo CSV está corrupto o mal formateado.')

except Exception as e:
    print(f'\nERROR inesperado: {e}')