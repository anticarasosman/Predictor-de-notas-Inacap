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
        internal_path = base_path / '_internal'
        
        print(f"[SETUP] Buscando TCL/TK desde: {internal_path}")
        
        # Buscar tcl8.6 (donde init.tcl está directamente)
        possible_tcl = [
            internal_path / 'tcl8.6',
            internal_path / 'tcl' / 'tcl8.6',
            base_path / 'tcl8.6',
        ]
        
        # Buscar tk8.6
        possible_tk = [
            internal_path / 'tk8.6',
            internal_path / 'tcl' / 'tk8.6',
            base_path / 'tk8.6',
        ]
        
        # Buscar y configurar TCL
        for tcl_path in possible_tcl:
            if tcl_path.exists():
                os.environ['TCL_LIBRARY'] = str(tcl_path)
                print(f"[SETUP] OK - TCL_LIBRARY: {tcl_path}")
                break
        else:
            print(f"[SETUP] WARN - TCL no encontrado")
        
        # Buscar y configurar TK
        for tk_path in possible_tk:
            if tk_path.exists():
                os.environ['TK_LIBRARY'] = str(tk_path)
                print(f"[SETUP] OK - TK_LIBRARY: {tk_path}")
                break
        else:
            print(f"[SETUP] WARN - TK no encontrado")


# Ejecutar setup apenas se importe este módulo
setup_tcl_tk()


