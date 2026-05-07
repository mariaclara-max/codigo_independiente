import pandas as pd
from pathlib import Path


def generate_transfer_file(
    input_file: str,
    output_folder: str,
    output_file: str,
    email_column: str = "Email",
    reason_text: str = "Usuario en lista negra"
):
    """
    Genera un CSV compatible entre consolas
    con estructura final:

    Email,Reason

    El archivo se guarda dentro de una carpeta destino.
    """

    try:
        # Crear carpeta de salida si no existe
        Path(output_folder).mkdir(
            parents=True,
            exist_ok=True
        )

        # Leer archivo CSV original
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

        # Ruta completa de salida
        output_path = Path(output_folder) / output_file

        # Guardar CSV final
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
# Carpeta donde se guardarán los nuevos CSV
# =====================================================

OUTPUT_FOLDER = "processed_csv"


# =====================================================
# SAAS -> PROMO
# =====================================================

generate_transfer_file(
    input_file="FROZEN_SAAS.csv",
    output_folder=OUTPUT_FOLDER,
    output_file="FROZEN_SAAS_TO_PROMO_TC.csv"
)
generate_transfer_file(
    input_file="INVALID_SAAS.csv",
    output_folder=OUTPUT_FOLDER,
    output_file="INVALID_SAAS_TO_PROMO_TC.csv"
)


# =====================================================
# PROMO -> SAAS
# =====================================================

generate_transfer_file(
    input_file="FROZEN_PROMO.csv",
    output_folder=OUTPUT_FOLDER,
    output_file="FROZEN_PROMO_TO_SAAS_TC.csv"
)
generate_transfer_file(
    input_file="INVALID_PROMO.csv",
    output_folder=OUTPUT_FOLDER,
    output_file="INVALID_PROMO_TO_SAAS_TC.csv"
)