# SAAS ↔ Promozione CSV 

Automated CSV transformation pipeline for transferring
frozen and blacklisted email records between platforms.

## Features
- CSV normalization
- Email extraction
- Reason column generation
- Daily archive folders
- Duplicate removal
- UTF-8 export compatibility
- Automated output structure

-------------------------------------

Script para dividir un archivo CSV grande en múltiples archivos
más pequeños utilizando pandas.

Características:
- Divide el archivo en bloques de tamaño configurable.
- Guarda cada bloque como un nuevo CSV.
- Crea automáticamente la carpeta de salida.
- Maneja errores comunes de lectura y formato.

Uso:
1. Colocar el archivo CSV en la misma carpeta del script.
2. Configurar:
   - Nombre del archivo
   - Número de filas por archivo
3. Ejecutar el script.

Salida:
Genera múltiples archivos CSV dentro de la carpeta output_parts.
