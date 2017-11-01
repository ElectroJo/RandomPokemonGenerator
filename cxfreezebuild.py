from cx_Freeze import setup, Executable

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [Executable("script.py", base = "Win32GUI")]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            ],
    },

}

setup(
    name = "Random Pokemon Generator and PSKM Sender",
    options = options,
    version = "0.07",
    description = 'Generate Random Pokemon and send them directly to PKSM',
    executables = executables
)
import shutil, errno
shutil.copytree('pokedex/pokedex/data/csv', 'build/exe.win32-3.6/pokedex/pokedex/data/csv')
shutil.copytree('Templates', 'build/exe.win32-3.6/Templates')
shutil.copy('Credits.txt', 'build/exe.win32-3.6/Credits.txt')
shutil.copytree('Images', 'build/exe.win32-3.6/Images')
shutil.copytree('sprites/sprites/pokemon', 'build/exe.win32-3.6/sprites/sprites/pokemon')
shutil.copytree('serveLegality-CLI/serveLegality/serveLegality/bin/Debug', 'build/exe.win32-3.6/serveLegality-CLI/serveLegality/serveLegality/bin/Debug')
shutil.rmtree('build/exe.win32-3.6/sprites/sprites/pokemon/back')
shutil.rmtree('build/exe.win32-3.6/sprites/sprites/pokemon/other-sprites')
shutil.rmtree('build/exe.win32-3.6/sprites/sprites/pokemon/model')