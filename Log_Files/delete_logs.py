import os
from pathlib import Path


def delete_textlog_parts() -> None:
    """Elimina todos los archivos .log dentro de la carpeta Source junto al script."""
    script_dir = Path(__file__).resolve().parent
    source_dir = script_dir / 'Source'
    pattern = '*.log'
    
    files = sorted(source_dir.glob(pattern))
    
    if not files:
        print(f'No se encontraron archivos .log en {source_dir} para eliminar.')
        return
    
    print(f'Se eliminarán {len(files)} archivo(s) en {source_dir}:')
    for f in files:
        print(f'  - {f.name}')
    
    confirm = input('\n¿Estás seguro? (s/n): ').strip().lower()
    if confirm != 's':
        print('Operación cancelada.')
        return
    
    deleted_count = 0
    for f in files:
        try:
            f.unlink()
            print(f'✓ Eliminado: {f.name}')
            deleted_count += 1
        except Exception as e:
            print(f'✗ Error al eliminar {f.name}: {e}')
    
    print(f'\nTotal eliminados: {deleted_count}/{len(files)}')


if __name__ == '__main__':
    delete_textlog_parts()
