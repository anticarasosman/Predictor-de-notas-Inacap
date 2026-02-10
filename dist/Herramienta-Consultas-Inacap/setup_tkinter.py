"""
Módulo para configurar correctamente Tcl/Tk y MySQL antes de importar.
Resuelve problemas comunes con PyInstaller en Windows.
"""

import os
import sys
import pathlib


def setup_environment():
    """
    Configura variables de entorno necesarias para Tkinter y MySQL.
    """
    
    print("[SETUP] ===== Iniciando configuración del entorno =====")
    
    # Detectar si estamos en una aplicación empaquetada por PyInstaller
    is_frozen = getattr(sys, 'frozen', False)
    
    if not is_frozen:
        print("[SETUP] Ejecutando desde Python directo (no congelado)")
        return
    
    # Estamos dentro de un .exe empaquetado
    base_path = pathlib.Path(sys.executable).parent
    internal_path = base_path / '_internal'
    
    print(f"[SETUP] Directorio base: {base_path}")
    print(f"[SETUP] Directorio _internal: {internal_path}")
    
    # ===== CONFIGURAR TCL/TK =====
    print("\n[SETUP] --- Configurando TCL/TK ---")
    
    # Buscar tcl8.6
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
    
    # Configurar TCL
    for tcl_path in possible_tcl:
        if tcl_path.exists():
            os.environ['TCL_LIBRARY'] = str(tcl_path)
            print(f"[SETUP] OK - TCL_LIBRARY: {tcl_path}")
            break
    else:
        print(f"[SETUP] WARN - TCL no encontrado")
    
    # Configurar TK
    for tk_path in possible_tk:
        if tk_path.exists():
            os.environ['TK_LIBRARY'] = str(tk_path)
            print(f"[SETUP] OK - TK_LIBRARY: {tk_path}")
            break
    else:
        print(f"[SETUP] WARN - TK no encontrado")
    
    # ===== CONFIGURAR MYSQL =====
    print("\n[SETUP] --- Configurando MySQL Connector ---")
    
    # Verificar dónde está mysql.connector
    locales_path = internal_path / 'mysql' / 'connector' / 'locales'
    if locales_path.exists():
        print(f"[SETUP] OK - MySQL locales encontrado: {locales_path}")
        # Listar lo que hay
        try:
            items = list(locales_path.iterdir())
            print(f"[SETUP]    Contenido: {', '.join([x.name for x in items[:5]])}")
        except:
            pass
    else:
        print(f"[SETUP] WARN - MySQL locales NO encontrado en: {locales_path}")
    
    # Verificar que existe eng.py o similar
    eng_file = locales_path / 'eng.py' if locales_path.exists() else None
    if eng_file and eng_file.exists():
        print(f"[SETUP] OK - Archivo eng.py encontrado")
    elif locales_path.exists():
        print(f"[SETUP] WARN - eng.py NO encontrado en locales/")
    
    print("\n[SETUP] ===== Configuración completada =====\n")


# Ejecutar setup apenas se importe este módulo
setup_environment()



