
import os
import ezFlashCLI

ezFlashfolder = os.path.dirname(ezFlashCLI.__file__)


def get_resources():
    data_files = []

    data_files.append((os.path.join(ezFlashfolder,'flash_database.json'),('.')))
    for r, d, f in os.walk(os.path.join('assets')):
        for file in f:
            data_files.append((os.path.join(r, file),r))

    for r, d, f in os.walk(os.path.join('frontend','dist','frontend')):
        for file in f:
            data_files.append((os.path.join(r, file),r))

    for r, d, f in os.walk(os.path.join(ezFlashfolder,'third-party','segger')):
        for file in f:
            data_files.append((os.path.join(r, file),'.'))

    return(data_files)
