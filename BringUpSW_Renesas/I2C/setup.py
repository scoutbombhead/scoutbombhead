from distutils.core import setup, Extension
setup(name = 'I2C', version = '1.0',  \
   ext_modules = [Extension('I2C', ['i2c_SMB.c', 'i2c.c'])])
