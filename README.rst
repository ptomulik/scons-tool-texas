scons-tool-texas
================

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

Copy the ``texas/`` directory to your project's ``site_scons/site_tools/`` or
to ``~/.scons/site_scons/site_tools/`` (per user configuration). See SCons manual
for details about installation of external tools. For full functionality you
may also need to install the `SCons dvipdfm tool`_.

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

TO DOWNLOAD DEPENDENCIES FROM EXTERNAL REPOSITORIES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it may be necessary to download files from other people's repositories,
for example test framework is necessary to run tests. We have some scripts to
automatize the download process, and they require the following software

  - mercurial_ VCS (``hg``),
  - git_ VCS (``git``).

TO RUN TESTS
^^^^^^^^^^^^

  - `SCons test framework`_ by Dirk Baechle, 
  - `SCons dvipdfm tool`_ by Paweł Tomulik

TO GENERATE API DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - epydoc_,
  - python-docutils_,
  - python-pygments_.

TO GENERATE USER DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - docbook-xml_,
  - xsltproc_,

and (locally downloaded)

  - `SCons docbook tool`_ by Dirk Baechle.

DOWNLOAD DEPENDENCIES FROM EXTERNAL REPOSITORIES
------------------------------------------------

Some files from external projects need to be downloaded into the
development tree (they are usually not a part of any installable package). The
files are obtainable from external repositories, and may be easily downloaded
on GNU systems with the script ``bin/download-deps.sh`` ::

    bin/download-deps.sh

The development tree may be later cleaned-up from the downloaded files by::

    bin/delete-deps.sh

Particular projects, that this project depends on, are mentioned in the
following subsections. You may look through it if the above scripts do not
work well on your platform. Otherwise, all of the following dependencies
are handled by ``download-deps.sh`` and ``delete-deps.sh`` scripts.  

All downloaded files are ignored by ``.gitignore``, so you don't have to worry
about deleting them before doing commits.

SCONS DVIPDFM TOOL
^^^^^^^^^^^^^^^^^^

The ``TeXAS`` tool depends on `SCons dvipdfm tool`_, which is not available in
the SCons_ core (at least not in 2.3.0 and earlier versions). The following
files/directories need to be downloaded (and placed as shown in table relative
to the top-level source directory)

 ========================= ==================================================
  source file/directory                   target file/directory
 ========================= ==================================================
   ``dvipdfm.py``            ``site_scons/site_tools/dvipdfm.py``
 ========================= ==================================================

On GNU systems you may download it with the script
``bin/download-dvipdfm-tool.sh``::

    bin/download-dvipdfm-tool.sh

The tool may be further removed from the development tree with the script
``bin/delete-dvipdfm-tool.sh``::

    bin/download-dvipdfm-tool.sh

TESTING FRAMEWORK
^^^^^^^^^^^^^^^^^

If you wish to run end-to-end tests for this tool, download the testing
framework for scons extensions/tools (currently from Dirk Baechle's repository
`SCons test framework`_ hosted on bitbucket.org). The following files/directories
need to be downloaded (and placed as shown in table relative to the top-level
source directory)

 ========================= ==================================================
  source file/directory                   target file/directory
 ========================= ==================================================
  ``QMTest/``               ``QMTest/``
 ------------------------- --------------------------------------------------
  ``runtest.py``            ``runtest.py``
 ========================= ==================================================

On GNU system you may use the ``bin/download-test-framework.sh``  script to
download the testing framework (requires ``hg`` to be installed on your system)::

    bin/download-test-framework.sh

This script downloads and copies to the top-level directory the ``QMTest``
package and ``runtest.py`` script from the repository. The test framework may
be later removed with the ``bin/delete-test-framework.sh`` script::

    bin/delete-test-framework.sh

You may also delete manually files/directories comprising the framework.


SCONS DOCBOOK TOOL
^^^^^^^^^^^^^^^^^^

If you wish to generate user's guide, you need to download locally the `scons
docbook tool`_. It is obtainable from Dirk Baechle's repository hosted on
bitbucket.org. The following files/directories need to be downloaded (and
placed as shown in table relative to the top-level source directory)

 ========================= =====================================================
  source file/directory                   target file/directory
 ========================= =====================================================
  ``__init__.py``           ``site_scons/site_tools/docbook/__init__.py``
 ------------------------- -----------------------------------------------------
  ``utils/``                ``site_scons/site_tools/docbook/utils``
 ------------------------- -----------------------------------------------------
  ``docbook-xsl-<ver>/``    ``site_scons/site_tools/docbook/docbook-xsl-<ver>``
 ========================= =====================================================

On GNU system you may use the ``bin/download-docbook-tool.sh``  script to
download the docbook tool (requires ``hg`` to be installed on your system)::

    bin/download-docbook-tool.sh

The tool may be later removed with the ``bin/delete-docbook-tool.sh`` script::

    bin/delete-test-framework.sh

You may also delete manually files/directories comprising the tool package.

RUNNING TESTS
-------------

To run all the tests type::
  
    python runtest.py -a

This requires the presence of the testing framework in the development tree.

GENERATING DOCUMENTATION
------------------------

Scons gnuplot tool has an API documentation and user manual. The documentation
may be generated as follows (see also REQUIREMENTS).

API DOCUMENTATION
^^^^^^^^^^^^^^^^^

To generate API documentation type::

    scons api-doc

The generated API documentation will be written to ``build/doc/api/``.

USER MANUAL
^^^^^^^^^^^

To generate user manual type::

    scons user-doc

The generated documentation will be written to ``build/doc/user/``.

LICENSE
-------
Copyright (c) 2013 by Pawel Tomulik

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
