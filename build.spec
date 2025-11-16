# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# 获取 pyzbar 的 DLL 文件路径
pyzbar_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'pyzbar')
pyzbar_dlls = [
    (os.path.join(pyzbar_path, 'libiconv.dll'), 'pyzbar'),
    (os.path.join(pyzbar_path, 'libzbar-64.dll'), 'pyzbar'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyzbar_dlls,
    datas=[],
    hiddenimports=[
        # PySide6 相关
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtNetwork',
        # qrcode 相关 - 添加所有子模块
        'qrcode',
        'qrcode.main',
        'qrcode.constants',
        'qrcode.util',
        'qrcode.exceptions',
        'qrcode.image',
        'qrcode.image.base',
        'qrcode.image.pure',
        'qrcode.image.pil',
        'qrcode.image.svg',
        'qrcode.image.styles',
        'qrcode.image.styles.moduledrawers',
        'qrcode.image.styles.moduledrawers.base',
        'qrcode.image.styles.colormasks',
        # MyQR 相关
        'MyQR',
        'MyQR.myqr',
        # barcode 相关
        'barcode',
        'barcode.writer',
        'barcode.codex',
        'barcode.ean',
        'barcode.ean13',
        'barcode.code39',
        'barcode.code128',
        # pyzbar 相关
        'pyzbar',
        'pyzbar.pyzbar',
        'pyzbar.wrapper',
        'pyzbar.locations',
        # PIL 相关
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.ImageColor',
        'PIL.ImageFilter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 使用目录模式（onedir），不使用单文件模式（onefile）
# 这样可以让 exe 文件更小，依赖文件分离在同一目录下
exe = EXE(
    pyz,
    a.scripts,
    [],  # 不包含 a.binaries, a.zipfiles, a.datas，这些会放在 COLLECT 中
    exclude_binaries=True,  # 关键：排除二进制文件，让它们分离
    name='QRCodeGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径，例如: 'icon.ico'
)

# COLLECT 用于收集所有依赖文件到一个目录中
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QRCodeGenerator',
)
