# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Get GDAL directory from environment
conda_prefix = os.environ.get('CONDA_PREFIX')
gdal_dir = os.path.join(conda_prefix, 'Library', 'bin')

# List of critical GDAL DLLs we need
critical_dlls = [
    'gdal.dll',
    'geos.dll',
    'geos_c.dll',
    'proj.dll',
    'sqlite3.dll',
    'libcrypto-1_1-x64.dll',
    'libssl-1_1-x64.dll',
    'zlib.dll'
]

# Collect specific GDAL binaries
gdal_dlls = []
for dll in critical_dlls:
    dll_path = os.path.join(gdal_dir, dll)
    if os.path.exists(dll_path):
        gdal_dlls.append((dll_path, '.'))

# Create a runtime hook to set up environment
with open('gdal_hook.py', 'w') as f:
    f.write("""
import os
import sys

# Set GDAL environment variables
os.environ['GDAL_DATA'] = os.path.join(sys._MEIPASS, 'Library', 'share', 'gdal')
os.environ['PROJ_LIB'] = os.path.join(sys._MEIPASS, 'Library', 'share', 'proj')
""")

a = Analysis(
    ['pytiff.py'],
    pathex=[gdal_dir],
    binaries=gdal_dlls,
    datas=[
        (os.path.join(conda_prefix, 'Library', 'share', 'proj'), 'Library/share/proj'),
        (os.path.join(conda_prefix, 'Library', 'share', 'gdal'), 'Library/share/gdal')
    ],
    hiddenimports=[
        'rasterio._shim', 
        'rasterio.control', 
        'rasterio._base', 
        'rasterio.sample',
        'osgeo.gdal',
        'osgeo.osr',
        'osgeo._gdal',
        'osgeo._osr',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['gdal_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pytiff',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 