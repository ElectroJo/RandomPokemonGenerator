from distutils.core import setup
import shutil, errno
import py2exe
setup(windows=['script.py'])
shutil.copytree('pokedex', 'dist/pokedex')
shutil.copy('base.pk7', 'dist/base.pk7')
shutil.copy('Newoutput.pk7', 'dist/Newoutput.pk7')
shutil.copy('outfile.pk7', 'dist/outfile.pk7')
shutil.copytree('Images', 'dist/Images')
shutil.copytree('sprites', 'dist/sprites')