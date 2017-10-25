from setuptools import setup, find_packages

# Read version from package.
from tablegroups.__version__ import __version__

setup(name='tablegroups',
      version=__version__,
      author='William Pfalzgraff',
      url="https://github.com/william-pfalzgraff/TableGroups/",
      use_2to3=False,
      license='LICENSE',
      description='A package for creating active learning groups.',
      packages=find_packages(),
      requires=['numpy', 'click'],
      entry_points={'console_scripts': ['tablegroups = tablegroups.__main__:cli']},
      test_suite="tablegroups.tests",
      )
