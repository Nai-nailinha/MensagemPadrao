# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MensagemPadrao.py'],
    pathex=[],
    binaries=[],
    datas=[('message_icon_new.ico', '.'), ('version.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MensagemPadrao',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\enailel\\PycharmProjects\\MensagemPadrao\\message_icon_new.ico'],
)
