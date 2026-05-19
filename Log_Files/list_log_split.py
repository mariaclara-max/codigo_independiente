import math

# Especifica el nombre del archivo de logs (solo el nombre, sin ruta)
file_name = 'bounces_reales_2.log'  # Cambia aquí el nombre del archivo si hace falta
# Construye la ruta usando la variable `file_name`
file_path = f'../../Downloads/{file_name}'

lines_per_file = 100000  # Cambia aquí el número de líneas que quieres por archivo

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Calcula cuántos archivos serán necesarios
num_files = math.ceil(len(lines) / lines_per_file)

# Divide las líneas en partes y guarda cada parte en un archivo .log separado
for i in range(num_files):
    start_row = i * lines_per_file
    end_row = start_row + lines_per_file
    part_lines = lines[start_row:end_row]
    # Guarda cada parte en un archivo .log diferente con el nuevo formato
    output_file_path = f'textlog_part{i + 1}.log'
    with open(output_file_path, 'w', encoding='utf-8') as out:
        out.writelines(part_lines)
    print(f'Parte {i + 1} guardada en {output_file_path}')

print(f'El archivo ha sido dividido en partes de {lines_per_file} líneas.')
