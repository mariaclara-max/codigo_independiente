# Database_Extraction

Este directorio contiene herramientas para extraer direcciones de correo de archivos de datos y trabajar con una estructura de carpetas `Source` y `Results`.

## Estructura de carpetas

- `Source/`: carpeta de entrada. Puede contener archivos y subcarpetas.
- `Results/`: carpeta de salida para los archivos CSV generados.

## Comportamiento clave

- El script `export_emails_from_csv.py` recorre todo el contenido de `Source`, incluyendo subcarpetas.
- Extrae todas las direcciones de correo encontradas en los archivos dentro de `Source`.
- Genera dos archivos CSV en `Results`:
  - `emails_unico.csv`: lista de emails únicos.
  - `emails_por_dominio.csv`: conteo de emails por dominio.

- El script `delete_source.py` borra todo el contenido de la carpeta `Source`, incluyendo subcarpetas.

## Uso

### Extraer emails

```bash
cd /Users/a/Desktop/Proyectos/Database_Extraction
python export_emails_from_csv.py
```

### Borrar todo el contenido de Source

```bash
cd /Users/a/Desktop/Proyectos/Database_Extraction
python delete_source.py
```

## Notas

- `Source` puede tener cualquier estructura de subcarpetas.
- Lo importante es el contenido completo de `Source`, no su estructura.
- `Results` se crea si no existe.
