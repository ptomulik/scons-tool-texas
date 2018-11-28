# -*- coding: utf-8 -*-
"""scons-tool-texas
"""

from setuptools import setup
import setuptools.command.install
import setuptools.command.develop
import os
import sys

if sys.version_info < (3, 0):
    from io import open as uopen
else:
    uopen = open

here = os.path.abspath(os.path.dirname(__file__))

readme_rst = os.path.join(here, 'README.rst')
with uopen(readme_rst, encoding='utf-8') as f:
    readme = f.read()

about = {}
about_py = os.path.join(here, 'about.py')
with open(about_py) as f:
    exec(f.read(), about)

class develop(setuptools.command.develop.develop):
    def _make_symlinks(self, sources):
        here = os.path.abspath(os.path.dirname(__file__))
        subdir = os.path.join(here, 'sconstool', 'texas')
        reldir = os.path.join(os.path.pardir, os.path.pardir)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        for source in sources:
            fullsrc = os.path.join(subdir, source)
            if not os.path.exists(fullsrc):
                target = os.path.join(reldir, source)
                os.symlink(target, fullsrc)
        readme_txt = os.path.join(subdir, 'README.txt')
        if not os.path.exists(readme_txt):
            with open(readme_txt, 'w') as f:
                f.write('This directory contains symlinks to workaround ' +
                        'broken "pip install -e ."')

    def run(self, *args, **kw):
        self._make_symlinks(['__init__.py', 'about.py',
                             'TeXASCommon.py', 'TeXASDist.py', 'TeXASDoc.py'])
        setuptools.command.develop.develop.run(self, *args, **kw)


install = setuptools.command.install.install


setup(
        name='scons-tool-texas',
        version=about['__version__'],
        package_dir={'sconstool.texas': '.'},
        packages=['sconstool.texas'],
        namespace_packages=['sconstool'],
        description='TeX Automated with SCons',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-texas',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl',
        cmdclass={'develop': develop, 'install': install},
        install_requires=['scons-tool-util >= 0.1.10',
                          'scons-tool-kpsewhich >= 0.1.1',
                          'scons-tool-dvipdfm >= 0.1.0',
                          'scons-tool-archives >= 0.1.1'],
        python_requires='>=2.7'
)

# vim: set expandtab tabstop=4 shiftwidth=4:
