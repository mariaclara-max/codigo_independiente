# CSV_Files

Este directorio contiene scripts para dividir y limpiar archivos CSV y logs relacionados con el procesamiento de datos.

## Archivos y funcionalidad

### `list_split.py`

- Divide un archivo CSV grande en varios archivos más pequeños llamados `part_{i}.csv`.
- El archivo de origen se define en la variable `file_name` y se lee desde `../../Downloads/` (cabe destacar que esta carpeta está contenida en una carpeta en Desktop, y a su vez, en una subcarpeta llamada 'CSV_Files', por lo que la ruta da dos saltos hacia arriba en el directorio).
- Cada parte contiene hasta `15,000` filas, modificable por el usuario.
- Las partes se guardan en la carpeta `CSV_Files/` donde está el script.

Uso:

```bash
python CSV_Files/list_split.py
```

> Cambia `file_name` en el script para usar otro CSV.

### `list_recover.py`

- Extrae un subconjunto de líneas de un archivo `.log` grande.
- El archivo de origen se define en la variable `file_name` y se lee desde `../../../Downloads/`.
- Toma las últimas líneas y las guarda en un archivo `file_{N}.log` (valor modificable por el usuario).
- También incluye una opción comentada para tomar las primeras líneas si se desea (valor modificable por el usuario).
- A la hora de ejecutar, se recomienda comentar una de las dos funciones para evitar funcionamiento síncrono.

Uso:

```bash
python CSV_Files/list_recover.py
```

> Ajusta `file_name`, `first_lines` y `last_lines` según necesites.

### `list_delete.py`

- Elimina todos los archivos `part_*.csv` generados por `list_split.py` en el mismo directorio.
- Ofrece dos modos:
  - Normal: pide confirmación antes de borrar.
  - `--yes` / `-y`: borra sin pedir confirmación.
  - `--dry-run`: muestra cuántos archivos se eliminarían sin borrar nada.

Uso:

```bash
python CSV_Files/list_delete.py
python CSV_Files/list_delete.py --yes
python CSV_Files/list_delete.py --dry-run
```

## Relación entre los scripts

- `list_split.py` es el único script que genera archivos `part_{i}.csv` en esta carpeta.
- `list_delete.py` se usa para limpiar esos archivos generados por `list_split.py`.
- `list_recover.py` es independiente y está pensado para extraer un fragmento de un archivo de log; no interactúa directamente con `list_split.py` o `list_delete.py`.

## Recomendaciones

- Ejecuta primero `list_split.py` para generar los `part_*.csv`.
- Si necesitas liberar espacio o reiniciar la carpeta, usa `list_delete.py`.
- `list_recover.py` sirve para preparar o reducir archivos de log antes de procesarlos con otras herramientas fuera de esta carpeta.
