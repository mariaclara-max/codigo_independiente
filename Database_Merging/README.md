# Database_Merging

Este directorio contiene un script para fusionar listas de emails de diferentes resultados y generar un informe consolidado.

## Script principal

- `merge_csv_databases.py`

## Qué hace

El script une los correos electrónicos de tres archivos CSV diferentes:

- `../Log_Files/Results/email_list.csv`
- `../Database_Extraction/Results/emails_list.csv`
- `../Log_Files/Results/telecom_email_list.csv`

## Reglas de fusión

- Omite duplicados usando una normalización a minúsculas.
- Solo se consideran correos válidos que contienen `@`.

## Salidas generadas

Los archivos de salida se guardan en `Database_Merging/Results`:

- `merged_emails.csv`: lista ordenada de emails únicos.
- `merged_emails_per_domain.csv`: conteo de emails por dominio.

## Uso

```bash
cd /Users/a/Desktop/Proyectos/Database_Merging
python merge_csv_databases.py
```

## Notas

- Si alguno de los archivos de entrada no existe, el script fallará con un error indicando el archivo faltante.
- La normalización de emails convierte todo a minúsculas para evitar duplicados por diferencias de mayúsculas/minúsculas.
