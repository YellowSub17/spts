from setuptools import setup, Extension
import numpy

setup(
ext_modules=[
Extension(
"spts.denoise",
sources=["spts/denoise_module.cpp"],
include_dirs=[numpy.get_include()],
),
Extension(
"spts.utils.fj",
sources=["spts/utils/fj/fj_module.cpp"],
include_dirs=[numpy.get_include()],
),
],
)
