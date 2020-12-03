# -*- mode: python ; coding: utf-8 -*-
import os
import pyuCommon
import site

from autoUpdate import APP_NAME

block_cipher = None



a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas= pyuCommon.get_resources(),
             hiddenimports=['engineio.async_drivers.threading'],
             hookspath=[os.path.join(site.getsitepackages()[-1],'pyupdater','hooks')],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=os.path.join('assets','link.ico') )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='win')
