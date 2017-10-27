from distutils.core import setup
import shutil, errno
import py2exe
setup(windows=['script.py'])
shutil.copytree('pokedex/pokedex/data/csv', 'dist/pokedex/pokedex/data/csv')
shutil.copy('base.pk7', 'dist/base.pk7')
shutil.copy('Newoutput.pk7', 'dist/Newoutput.pk7')
shutil.copy('outfile.pk7', 'dist/outfile.pk7')
shutil.copytree('Images', 'dist/Images')
shutil.copytree('sprites/sprites/pokemon', 'dist/sprites/sprites/pokemon')
shutil.rmtree('dist/sprites/sprites/pokemon/back')
shutil.rmtree('dist/sprites/sprites/pokemon/other-sprites')
shutil.rmtree('dist/sprites/sprites/pokemon/model')