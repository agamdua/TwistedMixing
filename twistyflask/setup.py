import sys
from setuptools import setup
from setuptools.command import egg_info
from setuptools.command.test import test as TestCommand

def _top_level(name):
    return name.split('.', 1)[0]

def _hacked_write_toplevel_names(cmd, basename, filename):
    names = map(_top_level, cmd.distribution.iter_distribution_names())
    pkgs = dict.fromkeys(set(names) - set(["twisted"]))
    cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

egg_info.write_toplevel_names = _hacked_write_toplevel_names

import re
versionLine = open("twistyflask/_version.py", "rt").read()
match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionLine, re.M)
versionString = match.group(1)

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

setup(name='twistyflask',
      version=versionString,
      description='A demo combining Twisted and Flask',
      long_description='A silly demo of a chat app that uses Flask, served by Twisted, with real-time chat features provided by txsockjs.',
      url="https://chiselapp.com/user/lvh/repository/TwistedMixing/home",

      author='Laurens Van Houtven',
      author_email='_@lvh.io',

      packages=["twistyflask", "twistyflask.test", "twisted.plugins"],
      test_suite="twistyflask.test",
      setup_requires=['tox'],
      cmdclass={'test': Tox},
      zip_safe=True,

      license='ISC',
      keywords="twisted flask",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Twisted",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
        ]
)

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
