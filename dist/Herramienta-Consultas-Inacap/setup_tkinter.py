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
        
        # Buscar los directorios de Tcl/Tk
        tcl_path = base_path / '_internal' / 'tcl'
        tk_path = base_path / '_internal' / 'tk'
        
        if tcl_path.exists():
            os.environ['TCL_LIBRARY'] = str(tcl_path)
            print(f"[DEBUG] TCL_LIBRARY set to: {tcl_path}")
        else:
            print(f"[WARN] TCL_LIBRARY not found at: {tcl_path}")
        
        if tk_path.exists():
            os.environ['TK_LIBRARY'] = str(tk_path)
            print(f"[DEBUG] TK_LIBRARY set to: {tk_path}")
        else:
            print(f"[WARN] TK_LIBRARY not found at: {tk_path}")
        
        # También intentar encontrar los datos de tcl/tk en otros lugares posibles
        alt_paths = [
            base_path / '_internal' / 'tkinter' / 'tcl',
            base_path / 'tcl',
            base_path / 'tk',
        ]
        
        for alt_path in alt_paths:
            if alt_path.exists() and 'TCL_LIBRARY' not in os.environ:
                os.environ['TCL_LIBRARY'] = str(alt_path)
                print(f"[DEBUG] Found TCL at alternative location: {alt_path}")
                break


# Ejecutar setup apenas se importe este módulo
setup_tcl_tk()
