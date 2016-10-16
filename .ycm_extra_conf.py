"""YCM configuration for evalpac."""

import subprocess
from numpy.distutils.misc_util import get_numpy_include_dirs

def FlagsForFile(filename, **kwargs):
    flags = [
        '-fopenmp',
    ]
    flags.extend(subprocess.check_output(
        ['python3-config', '--include'], universal_newlines=True
    ).split())
    flags.extend(
        '-I' + i for i in get_numpy_include_dirs()
    )

    return {'flags': flags}
