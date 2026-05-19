import os
import shutil
from pathlib import Path

SOURCE_DIR = Path("Source")

def delete_source_content():
    """Borra todo el contenido de la carpeta Source, incluyendo subcarpetas."""
    
    if not SOURCE_DIR.exists():
        print(f"La carpeta {SOURCE_DIR} no existe.")
        return
    
    # Confirmación de seguridad
    print(f"⚠️  ADVERTENCIA: Se va a borrar todo el contenido de '{SOURCE_DIR}' incluyendo subcarpetas.")
    print(f"Archivos a eliminar: {len(list(SOURCE_DIR.rglob('*')))}")
    response = input("\n¿Estás seguro? (s/n): ").strip().lower()
    
    if response != 's':
        print("Operación cancelada.")
        return
    
    try:
        # Borrar el contenido
        for item in SOURCE_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
                print(f"✓ Carpeta eliminada: {item.name}")
            else:
                item.unlink()
                print(f"✓ Archivo eliminado: {item.name}")
        
        print(f"\n✓ Todo el contenido de '{SOURCE_DIR}' ha sido eliminado correctamente.")
    
    except Exception as e:
        print(f"✗ Error al eliminar: {e}")

if __name__ == "__main__":
    delete_source_content()
