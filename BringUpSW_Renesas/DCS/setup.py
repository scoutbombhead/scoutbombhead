from distutils.core import setup, Extension
setup(name = 'DU', version = '1.0',  \
   ext_modules = [Extension('DCS', ['dcs.c', 'video_capture.c'])])
