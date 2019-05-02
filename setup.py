# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:01:10 2019

@author: 王一晨
"""

import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
 
filename = 'test' # 源文件名
full_filename = 'test.pyx' # 包含后缀的源文件名
 
setup(
    name = 'test',
    cmdclass = {'build_ext': build_ext},
    ext_modules=[Extension(filename,sources=[full_filename, "main.c"],
                 include_dirs=[numpy.get_include()])],
)
