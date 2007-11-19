#!/usr/bin/env python

from distutils.core import setup, Extension

phoenix_extension = Extension('phoenix_driver',
	include_dirs = ['.'],
	sources=['py_parse.c', 'parse.c', 'match.c', 'grammar.c', 'dict.c', 'pconf.c', 'print_structs.c'])

setup(name='PyPhoenix',
	version='1.0',
	description='A python interface for phoenix',
	author='Jesse Lovelace',
	py_modules=['phoenix'],
	author_email='jesse.lovelace@gmail.com',
	url='http://hawatian.com/',
	ext_modules=[phoenix_extension]
)
