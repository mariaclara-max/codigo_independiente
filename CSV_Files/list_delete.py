import argparse
from pathlib import Path


def delete_part_csv_files(dry_run: bool = False, yes: bool = False) -> int:
    """Elimina todos los archivos part_*.csv en el mismo directorio del script."""
    script_dir = Path(__file__).resolve().parent
    pattern = 'part_*.csv'
    files = sorted(script_dir.glob(pattern))

    if not files:
        print('No se encontraron archivos part_*.csv para eliminar.')
        return 0

    if dry_run:
        print(f'DRY RUN: se encontraron {len(files)} archivos part_*.csv.')
        return 0

    if not yes:
        confirm = input('¿Estás seguro de que quieres eliminar todos los archivos part_*.csv? (s/n): ').strip().lower()
        if confirm != 's':
            print('Operación cancelada.')
            return 0

    deleted_count = 0
    for f in files:
        try:
            f.unlink()
            deleted_count += 1
        except Exception:
            pass

    print(f'Total eliminados: {deleted_count}/{len(files)}')
    return deleted_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Elimina todos los archivos part_*.csv generados por list_split.py en este directorio.'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Eliminar sin pedir confirmación.',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar qué se eliminaría sin borrar nada.',
    )
    args = parser.parse_args()

    delete_part_csv_files(dry_run=args.dry_run, yes=args.yes)


if __name__ == '__main__':
    main()
