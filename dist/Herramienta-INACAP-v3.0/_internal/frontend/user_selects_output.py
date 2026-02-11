import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def select_output_directory(title="Selecciona la carpeta de destino"):
    """
    Abre un diálogo para que el usuario seleccione una carpeta de destino.
    
    Args:
        title: Título del diálogo de selección
        
    Returns:
        Path: Ruta de la carpeta seleccionada, o None si se cancela
    """
    # Crear una ventana raíz temporal (invisible)
    root = tk.Tk()
    root.withdraw()
    
    # Abrir diálogo de selección de carpeta
    folder_path = filedialog.askdirectory(title=title)
    
    # Destruir la ventana temporal
    root.destroy()
    
    # Retornar Path object o None si se canceló
    return Path(folder_path) if folder_path else None


def clean_previous_files(output_dir, filename_pattern):
    """
    Limpia archivos previos que coincidan con el patrón especificado.
    
    Args:
        output_dir: Directorio donde limpiar archivos
        filename_pattern: Patrón glob para identificar archivos a eliminar
    """
    output_dir = Path(output_dir)
    
    if not output_dir.exists():
        return
    
    for file in output_dir.glob(filename_pattern):
        try:
            file.unlink()
            print(f"✓ Archivo eliminado: {file.name}")
        except Exception as e:
            print(f"✗ No se pudo eliminar {file.name}: {str(e)}")
