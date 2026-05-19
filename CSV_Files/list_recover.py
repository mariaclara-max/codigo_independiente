# Especifica el nombre del archivo de logs (solo el nombre, sin ruta)
file_name = 'Mistral_Tamigi_Newsletter_02_All_Tags_Buona_part_2.log'  # Cambia aquí el nombre del archivo si hace falta

# Construye la ruta usando la variable `file_name`
file_path = f'../../../Downloads/{file_name}'

# Coger primeras X líneas
# first_lines = 1234567890

# Coger ultimas X líneas
last_lines = 1234567890

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
	lines = f.readlines()

# Coger primeros X líneas (descomentar si se quiere)
# selected = lines[:first_lines]

# Coger ultimas X líneas (descomentar si se quiere)
selected = lines[-last_lines:]

# Guardar
output_file = f'file_{len(selected)}.log'
with open(output_file, 'w', encoding='utf-8') as out:
	out.writelines(selected)

print("Líneas:", len(selected))