"""
Módulo para configurar correctamente Tcl/Tk antes de importar Tkinter.
Resuelve problemas comunes con PyInstaller y Tkinter en Windows.
"""

import os
import sys
import pathlib


def setup_tcl_tk():
    """
    Configura las variables de entorno de Tcl/Tk para que funcione correctamente
    en aplicaciones empaquetadas con PyInstaller.
    """
    
    # Detectar si estamos en una aplicación empaquetada por PyInstaller
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        # Estamos dentro de un .exe empaquetado
        base_path = pathlib.Path(sys.executable).parent
        
        print(f"[SETUP] Buscando TCL/TK desde: {base_path}")
        
        # Buscar en múltiples ubicaciones posibles
        possible_locations_tcl = [
            base_path / '_internal' / 'tcl',
            base_path / 'tcl',
            base_path.parent / '_internal' / 'tcl',
            base_path.parent / 'tcl',
        ]
        
        possible_locations_tk = [
            base_path / '_internal' / 'tk',
            base_path / 'tk',
            base_path.parent / '_internal' / 'tk',
            base_path.parent / 'tk',
        ]
        
        # Buscar y configurar TCL
        for tcl_path in possible_locations_tcl:
            if tcl_path.exists():
                os.environ['TCL_LIBRARY'] = str(tcl_path)
                print(f"[SETUP] ✓ TCL_LIBRARY configurado: {tcl_path}")
                break
        else:
            print(f"[SETUP] ✗ TCL no encontrado en ninguna ruta")
        
        # Buscar y configurar TK
        for tk_path in possible_locations_tk:
            if tk_path.exists():
                os.environ['TK_LIBRARY'] = str(tk_path)
                print(f"[SETUP] ✓ TK_LIBRARY configurado: {tk_path}")
                break
        else:
            print(f"[SETUP] ✗ TK no encontrado en ninguna ruta")


# Ejecutar setup apenas se importe este módulo
setup_tcl_tk()

