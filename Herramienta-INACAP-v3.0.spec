# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para Herramienta INACAP v3.0
Modo: onedir (carpeta con archivos)
Python: 3.13
Fecha: Febrero 2026
"""

import sys
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluir carpeta de datos (CSV)
        ('data', 'data'),
        # Incluir frontend (recursos si existen)
        ('frontend', 'frontend'),
        # Incluir clases
        ('classes', 'classes'),
        # Incluir base de datos (scripts SQL)
        ('database', 'database'),
        # Archivos de configuración
        ('.env.example', '.'),
    ],
    hiddenimports=[
        # MySQL Connector
        'mysql.connector',
        'mysql.connector.locales',
        'mysql.connector.abstracts',
        'mysql.connector.plugins',
        'mysql.connector.plugins.mysql_auth_plugin',
        'mysql.connector.plugins.mysql_native_password',
        # Pandas y dependencias
        'pandas',
        'pandas._libs.tslibs.offsets',
        'numpy',
        # Openpyxl (Excel) - TODO
        'openpyxl',
        'openpyxl.compat',
        'openpyxl.compat.itertools',
        'openpyxl.styles',
        'openpyxl.styles.fonts',
        'openpyxl.styles.colors',
        'openpyxl.styles.borders',
        'openpyxl.styles.fills',
        'openpyxl.styles.alignment',
        'openpyxl.styles.numbers',
        'openpyxl.worksheet',
        'openpyxl.worksheet.datavalidation',
        'openpyxl.worksheet.worksheet',
        'openpyxl.worksheet.table',
        'openpyxl.utils',
        'openpyxl.utils.datetime',
        'openpyxl.drawing',
        'openpyxl.drawing.image',
        # PDF
        'PyPDF2',
        # Otros
        'dotenv',
        'chardet',
    ],
    hookspath=[],  # No usar hooks locales por defecto
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        'tests',
        'testing',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Herramienta-INACAP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Herramienta-INACAP-v3.0',  # Nombre de la carpeta
)
