import os
from pathlib import Path


def delete_textlog_parts() -> None:
    """Elimina todos los archivos textlog_part*.log del directorio actual."""
    script_dir = Path(__file__).resolve().parent
    pattern = 'textlog_part*.log'
    
    files = sorted(script_dir.glob(pattern))
    
    if not files:
        print('No se encontraron archivos textlog_part*.log para eliminar.')
        return
    
    print(f'Se eliminarán {len(files)} archivo(s):')
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
