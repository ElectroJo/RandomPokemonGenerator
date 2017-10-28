from distutils.core import setup
import shutil, errno
import py2exe
setup(windows=['script.py'])
shutil.copytree('pokedex/pokedex/data/csv', 'dist/pokedex/pokedex/data/csv')
shutil.copytree('Templates', 'dist/Templates')
shutil.copy('Credits.txt', 'dist/Credits.txt')
shutil.copytree('Images', 'dist/Images')
shutil.copytree('sprites/sprites/pokemon', 'dist/sprites/sprites/pokemon')
shutil.copytree('serveLegality-CLI/serveLegality/serveLegality/bin/Debug', 'dist/serveLegality-CLI/serveLegality/serveLegality/bin/Debug')
shutil.rmtree('dist/sprites/sprites/pokemon/back')
shutil.rmtree('dist/sprites/sprites/pokemon/other-sprites')
shutil.rmtree('dist/sprites/sprites/pokemon/model')