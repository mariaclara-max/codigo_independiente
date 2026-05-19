import pandas as pd
import math
from pathlib import Path
 
# Especifica el nombre del archivo CSV (solo el nombre, sin ruta)
file_name = 'mytrack04.csv'  # Cambia aquí el nombre del archivo si hace falta
# Construye la ruta usando la variable `file_name`
file_path = f'../../Downloads/{file_name}'
 
# Lee el archivo CSV en un DataFrame
df = pd.read_csv(file_path)
 
# Define el número de filas por archivo
emails_per_file = 15000
 
# Calcula cuántos archivos serán necesarios
num_files = math.ceil(len(df) / emails_per_file)

# Obtiene la carpeta donde está este script
script_dir = Path(__file__).resolve().parent

# Divide el DataFrame en partes y guarda cada parte en un archivo CSV separado
for i in range(num_files):
    start_row = i * emails_per_file
    end_row = start_row + emails_per_file
    df_part = df.iloc[start_row:end_row]
    # Guarda cada parte en un archivo CSV diferente
    output_file_path = script_dir / f'part_{i + 1}.csv'
    df_part.to_csv(output_file_path, index=False)
    print(f'Parte {i + 1} guardada en {output_file_path}')
 
print("El archivo ha sido dividido en partes de 15,000 correos electrónicos.")