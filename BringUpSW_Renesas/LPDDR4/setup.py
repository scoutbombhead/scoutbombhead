from distutils.core import setup, Extension
setup(name = 'DDR4', version = '1.0',  \
   ext_modules = [Extension('DDR4', ['ddr4.c', 'lpddr4.c'])])
