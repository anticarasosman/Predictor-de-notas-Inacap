# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para Herramienta INACAP v3.0
Modo: onedir (carpeta con archivos)
Python: 3.13
Fecha: Febrero 2026
"""

import sys
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Incluir TODOS los submódulos de mysql.connector.locales
mysql_locales = collect_submodules('mysql.connector.locales')

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
        # Sistema de encriptación
        ('config_loader.py', '.'),
        ('.env.encrypted', '.'),
    ],
    hiddenimports=[
        # API Gateway / AWS
        'requests',
        'urllib3',
        'certifi',
        'boto3',
        'botocore',
        # AWS API Client
        'aws.api_client',
        # MySQL Connector (para compatibilidad/fallback)
        'mysql.connector',
        'mysql.connector.locales',
        'mysql.connector.locales.eng',
        'mysql.connector.abstracts',
        'mysql.connector.plugins',
        *mysql_locales,
        # Pandas y dependencias
        'pandas',
        'pandas._libs.tslibs.offsets',
        'numpy',
        # Openpyxl (Excel)
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
        # Encriptación
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.backends',
    ],
    hookspath=['.'],  # Incluir hooks personalizados del directorio actual
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
    console=False,  # TEMPORAL: Activar consola para diagnóstico
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
