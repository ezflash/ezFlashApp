# -*- mode: python ; coding: utf-8 -*-
import os
import ezFlashCLI
import pyuCommon
import site

ezFlashfolder = os.path.dirname(ezFlashCLI.__file__)
block_cipher = None

from autoUpdate import APP_NAME

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
          name='mac',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mac')
app = BUNDLE(coll,
            name='{}.app'.format(APP_NAME),
            icon='assets/link.icns',
            bundle_identifier='org.ezflash.{}'.format(APP_NAME),
            info_plist = {
                'NSRequiresAquaSystemAppearance': 'No'
            })
