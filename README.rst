scons-tool-texas
================

.. image:: https://badge.fury.io/py/scons-tool-texas.svg
    :target: https://badge.fury.io/py/scons-tool-texas
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-texas.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-texas
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-texas?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-texas

This is a SCons tool (set) named TeX Automated with SCons (``TeXAS``). It
wraps several SCons builders with the aim of simplifying compilation of ``TeX``
projects. It brings several features, that you may find useful:

- compact syntax,
- consistent interface between builders provided by ``TeXAS``,
- oriented towards compiling named "projects",
- automatic generation of SCons aliases for predefined targets,
- automatic deduction of target file names based on project name,
- builders for creating tarballs with document sources,
- support for VariantDir,

INSTALLATION
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add texas tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-texas

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-texas

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-texas = "*"


The tool will be installed as a namespaced package ``sconstool.texas``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-texas`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-texas.git site_scons/site_tools/texas

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.texas`` (this may be required by other tools).

USAGE EXAMPLE
-------------

Assume you have a paper named ``'foo'`` which compiles from single source
``foo.tex``. The paper's current version is ``1.0``. The source file
``foo.tex`` includes ``bar.tex`` which, in turn, includes ``bar.eps`` image.
You're unsure, whether LaTeX scanner adds ``bar.eps`` to implicit dependencies
or not. To compile paper and distribute its sources (for editorial manager
e.g.) you may write simple SCons script::

    # SConstruct
    env = Environment(tools = ['texas'])
    dvi = env.TeXASDVI('foo', version = '1.0', dvi_deps = ['bar.eps'])
    src = env.TeXASRmDup( dvi[0].children() )
    tar = env.TeXASTarGz('foo', src, version = '1.0')

You may compile entire project, or just parts of it::

    scons -Q         # build all (papers)
    scons -Q foo-dvi # Build only foo-1.0.dvi
    scons -Q foo-tgz # Create only the source tarball foo-1.0.tar.gz
    scons -Q foo     # Build paper 'foo' (there may be more in the source tree)

For more examples, see user manual (see the section `GENERATING DOCUMENTATION`_).

PREREQUISITES
-------------

To perform certain activities, you may need the following packages (listed per
task).

TO GENERATE API DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - epydoc_,
  - python-docutils_,
  - python-pygments_.

TO GENERATE USER DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - docbook-xml_,
  - xsltproc_,

GENERATING DOCUMENTATION
------------------------

Scons gnuplot tool has an API documentation and user manual. The documentation
may be generated as follows (see also REQUIREMENTS).

API DOCUMENTATION
^^^^^^^^^^^^^^^^^

To generate API documentation type::

    pipenv run scons api-doc

The generated API documentation will be written to ``build/doc/api/``.

USER MANUAL
^^^^^^^^^^^

To generate user manual type::

    pipenv run scons user-doc

The generated documentation will be written to ``build/doc/user/``.

LICENSE
-------
Copyright (c) 2013-2020 by Paweł Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _scons: http://scons.org
.. _`SCons test framework`: https://bitbucket.org/dirkbaechle/scons_test_framework
.. _mercurial: http://mercurial.selenic.com/
.. _epydoc: http://epydoc.sourceforge.net/
.. _python-docutils: http://pypi.python.org/pypi/docutils
.. _python-pygments: http://pygments.org/
.. _docbook-xml: http://www.oasis-open.org/docbook/xml/
.. _xsltproc: http://xmlsoft.org/libxslt/
.. _SCons docbook tool: https://bitbucket.org/dirkbaechle/scons_docbook/
.. _git: http://git-scm.com/
.. _SCons dvipdfm tool: https://github.com/ptomulik/scons-tool-dvipdfm
.. _SCons kpsewhich tool: https://github.com/ptomulik/scons-tool-kpsewhich
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
