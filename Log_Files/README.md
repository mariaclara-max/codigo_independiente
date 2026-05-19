# Log_Files

Este directorio contiene herramientas para dividir y procesar archivos de log, con un flujo de trabajo basado en carpetas `Source`, `Results` y `Config Files`.

## Estructura de carpetas

- `Source/`: guarda los archivos `.log` de entrada que se procesarán.
- `Results/`: guarda los CSV resultantes generados por `take_emails_from_log.py`.
- `Config Files/`: contiene listas de dominios usados para filtrar resultados.

## Archivos Python

### `list_log_split.py`

- Divide un archivo `.log` grande en archivos más pequeños llamados `textlog_part{N}.log`.
- El archivo de origen se define en `file_name` y se lee desde `../../Downloads/`.
- El número de líneas por archivo se define en `lines_per_file`.
- Genera los archivos `textlog_part1.log`, `textlog_part2.log`, etc. en la carpeta `Log_Files/Source`.

Uso:

```bash
cd /Users/a/Desktop/Proyectos/Log_Files
python list_log_split.py
```

### `take_emails_from_log.py`

- Procesa todos los archivos `.log` que hay en `Log_Files/Source`.
- Extrae correos electrónicos receptores.
- Determina la codificación de cada registro según `Content-Transfer-Encoding`.
- Muestra un informe por archivo en terminal con conteos de:
  - Standard emails
  - Telecom emails
  - Forbidden emails descartados
- Crea dos CSV sin duplicados en `Log_Files/Results`:
  - `emails_con_codificacion.csv` para dominios estándar.
  - `telecom_emails_con_codificacion.csv` para dominios listados en `Config Files/telecom_domains.log`.
- Omite correos cuyo dominio aparece en `Config Files/forbidden_domains.log`.

Uso:

```bash
cd /Users/a/Desktop/Proyectos/Log_Files
python take_emails_from_log.py
```

### `delete_logs.py`

- Elimina los archivos `textlog_part*.log` generados en `Log_Files/Source`.
- Pide confirmación antes de eliminar.

Uso:

```bash
cd /Users/a/Desktop/Proyectos/Log_Files
python delete_logs.py
```

## Archivos de configuración

- `Config Files/telecom_domains.log`: dominios que se consideran telecom. Los emails de estos dominios se escriben en `telecom_emails_con_codificacion.csv`.
- `Config Files/forbidden_domains.log`: dominios vetados. Los emails de estos dominios se descartan completamente.

## Flujo de trabajo

1. Ejecuta `list_log_split.py` para dividir un log grande en `Log_Files/Source`.
2. Ejecuta `take_emails_from_log.py` para extraer emails y codificación.
3. Revisa los archivos CSV en `Log_Files/Results`.
4. Usa `delete_logs.py` para limpiar los archivos temporales en `Log_Files/Source`.

## Notas importantes

- `take_emails_from_log.py` trabaja con todos los logs presentes en `Source`.
- El resultado se guarda en CSV, no en formato log.
- Los CSV no contienen entradas duplicadas.
- Los dominios prohibidos no aparecen en ningún CSV.
