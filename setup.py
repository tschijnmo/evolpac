import numpy.distutils.misc_util
from setuptools import setup, Extension, find_packages

numpy_includes = numpy.distutils.misc_util.get_numpy_include_dirs()
duel = Extension(
    "evolpac.duel.duel",
    ["evolpac/duel/duel.c", "evolpac/duel/PacWarGuts.c"],
    include_dirs=numpy_includes
)
tournament = Extension(
    "evolpac.duel.tournament",
    ["evolpac/duel/tournament.c", "evolpac/duel/PacWarGuts.c"],
    include_dirs=numpy_includes,
)

setup(
    name='evolpac',
    version='0.1',
    description='Evolutionary optimization of PAC-mites',
    author='Shuo Zhao',
    author_email='zhaoshuosve@gmail.com',
    ext_modules=[tournament, duel],
    packages=find_packages(),
    install_requires=['numpy']
)
