# Log_Files

Este directorio contiene herramientas para dividir, procesar y limpiar archivos de log, junto con archivos de configuración que definen dominios telecom y dominios vetados.

## Archivos Python

### `list_log_split.py`

- Divide un archivo `.log` grande en archivos más pequeños llamados `textlog_part{N}.log`.
- El archivo de origen se define en `file_name` y se lee desde `../../Downloads/` (cabe destacar que esta carpeta está contenida en una carpeta en Desktop, y a su vez, en una subcarpeta llamada 'Log_Files', por lo que la ruta da dos saltos hacia arriba en el directorio).
- El número de líneas por archivo se define en `lines_per_file`.
- Genera los archivos `textlog_part1.log`, `textlog_part2.log`, etc. en el directorio `Log_Files/`.

Uso:

```bash
python Log_Files/list_log_split.py
```

### `take_emails_from_log.py`

- Procesa archivos `textlog_part{N}.log` y extrae direcciones de correo receptoras.
- Detecta direcciones en los encabezados `To:`, `Cc:`, `Delivered-To:` y otros, más búsquedas fallback en el contenido.
- Clasifica resultados en:
  - `extracted_mails.log` para otros dominios
  - `extracted_telecom_mails.log` para dominios telecom
- Evita entradas duplicadas por `email|encoding` cuando no se usa `--no-dedupe`.
- Omite entradas cuyos dominios están en la blacklist de `Config Files/forbidden_domains.log`.
- Permite procesar un archivo específico o todos los archivos `textlog_part*.log` con `max_num + 1`.

Uso:

```bash
python Log_Files/take_emails_from_log.py 1
python Log_Files/take_emails_from_log.py --output-file=salida.log
python Log_Files/take_emails_from_log.py 16  # para 16 == max_num+1, procesa todos
```

Opciones relevantes:

- `--output-file`, `-o`: nombre del archivo de salida principal.
- `--telecom-output-file`: archivo de salida para dominios telecom.
- `--telecom-domains-file`: ruta al archivo de dominios telecom.
- `--forbidden-mails-file`: ruta al archivo de dominios vetados.
- `--no-dedupe`: permite duplicados.

### `delete_logs.py`

- Elimina todos los archivos `textlog_part*.log` del directorio `Log_Files/`.
- Pide confirmación antes de borrarlos.

Uso:

```bash
python Log_Files/delete_logs.py
```

## Archivos de configuración

Los archivos en `Log_Files/Config Files/` no se tocan habitualmente; sirven como definición de parámetros:

- `telecom_domains.log`: lista de dominios considerados telecom. `take_emails_from_log.py` carga estos dominios para separar la salida telecom.
- `forbidden_domains.log`: lista de dominios vetados. `take_emails_from_log.py` descarta cualquier correo cuyo dominio esté en esta lista.

## Flujo de trabajo cruzado

1. `list_log_split.py` divide un log grande en partes manejables `textlog_part{N}.log`.
2. `take_emails_from_log.py` procesa cada parte y extrae las direcciones receptoras.
3. `delete_logs.py` se usa cuando ya no se necesitan los archivos `textlog_part*.log` creados por `list_log_split.py`.

Los archivos dentro de `Config Files/` influyen solo en `take_emails_from_log.py`:

- `telecom_domains.log` define qué dominios van a `extracted_telecom_mails.log`
- `forbidden_domains.log` define qué entradas se descartan completamente

## Recomendaciones

- Ajusta `file_name` y `lines_per_file` en `list_log_split.py` antes de ejecutar.
- Ejecuta `take_emails_from_log.py` sobre archivos generados por `list_log_split.py`.
- Usa `delete_logs.py` cuando quieras limpiar los archivos de partición.
