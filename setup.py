import numpy.distutils.misc_util
from setuptools import setup, Extension, find_packages

pypacwar = Extension(
    "evolpac.duel._PyPacwar",
    ["evolpac/duel/PyPacwar.c", "evolpac/duel/PacWarGuts.c"],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs()
)

setup(
    name='evolpac',
    version='0.1',
    description='Evolutionary optimization of PAC-mites',
    author='Shuo Zhao',
    author_email='zhaoshuosve@gmail.com',
    ext_modules=[pypacwar],
    packages=find_packages(),
    install_requires=['numpy']
)
