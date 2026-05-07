import pandas as pd
from pathlib import Path
from datetime import datetime


def generate_transfer_file(
    input_file: str,
    output_folder: Path,
    output_file: str,
    email_column: str = "Email",
    reason_text: str = "Usuario en lista negra"
):
    """
    Genera un CSV compatible entre consolas
    con estructura final:

    Email,Reason

    Guarda el archivo dentro de una carpeta diaria.
    """

    try:
        # Leer CSV original
        df = pd.read_csv(
            input_file,
            dtype=str,
            encoding="utf-8"
        )

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        # Validar columna Email
        if email_column not in df.columns:
            raise ValueError(
                f"No existe la columna '{email_column}' en el archivo {input_file}"
            )

        # Crear DataFrame final
        export_df = pd.DataFrame()

        export_df["Email"] = df[email_column]

        export_df["Reason"] = reason_text

        # Eliminar emails vacíos
        export_df = export_df.dropna(subset=["Email"])

        # Limpiar espacios
        export_df["Email"] = export_df["Email"].str.strip()

        # Eliminar filas vacías
        export_df = export_df[
            export_df["Email"] != ""
        ]

        # Eliminar duplicados
        export_df = export_df.drop_duplicates()

        # Ruta final archivo
        output_path = output_folder / output_file

        # Guardar CSV
        export_df.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"Archivo generado correctamente:")
        print(output_path)

    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {input_file}")

    except pd.errors.EmptyDataError:
        print(f"ERROR: El archivo {input_file} está vacío")

    except Exception as e:
        print(f"ERROR procesando {input_file}: {e}")


# =====================================================
# CREAR CARPETA DIARIA
# =====================================================

# Fecha actual
today = datetime.now().strftime("%Y-%m-%d")

# Carpeta base
base_folder = Path("processed_csv")

# Carpeta diaria
daily_folder = base_folder / f"processed_csv_{today}"

# Crear carpetas automáticamente
daily_folder.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Carpeta del día creada:")
print(daily_folder)


# =====================================================
# SAAS -> PROMO
# =====================================================

generate_transfer_file(
    input_file="FROZEN_SAAS.csv",
    output_folder=daily_folder,
    output_file="FROZEN_SAAS_TO_PROMO_TC.csv"
)
generate_transfer_file(
    input_file="INVALID_SAAS.csv",
    output_folder=daily_folder,
    output_file="INVALID_SAAS_TO_PROMO_TC.csv"
)


# =====================================================
# PROMO -> SAAS
# =====================================================

generate_transfer_file(
    input_file="FROZEN_PROMO.csv",
    output_folder=daily_folder,
    output_file="FROZEN_PROMO_TO_SAAS_TC.csv"
)
generate_transfer_file(
    input_file="INVALID_PROMO.csv",
    output_folder=daily_folder,
    output_file="INVALID_PROMO_TO_SAAS_TC.csv"
)
