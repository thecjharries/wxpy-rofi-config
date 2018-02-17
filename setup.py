from os.path import join
from setuptools import setup, find_packages

with open(join('wxpy_rofi_config', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

setup(
    name='wxpy-rofi-config',
    version=__version__,
    packages=find_packages(),
    package_data={
        '': [
            'VERSION',
        ]
    },
    include_package_data=True
)
