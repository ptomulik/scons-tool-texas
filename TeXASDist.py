# -*- coding: utf-8 -*-
"""`texas.TeXASDist`

Utility functions for packaging and distribution of sources.
"""

#
# Copyright (c) 2013-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

from . import TeXASCommon

_local_keywords = TeXASCommon.keywords + [
    'strip_dirs'
]

def _del_local_keywords(kw):
    global _local_keywords
    return TeXASCommon.del_keys(kw, _local_keywords)

def _tar(env, name, source, **kw):
    """Core of the `Tar()`, `TarGz()` and `TarBz2()`"""
    import SCons.Util
    import platform

    target = TeXASCommon.get_auto_target(env, name, **kw)
    alias = TeXASCommon.get_auto_alias(name, 'alias', **kw)

    # Some paths are stripped from file names in the archive
    dirs2strip = TeXASCommon.get_strip_dirs(env, **kw)

    target = env.TarFile(target, source, TARFILEMAPPINGS=dirs2strip, **kw)

    if alias:
        env.Alias(alias, target)
        env.AlwaysBuild(alias)
    return target

def Tar(env, name, source, **kw):
    """Create tar archive from source(s).

    This function creates TAR archive containing files listed in the ``source``
    argument. The target file name may be fixed with the ``target`` argument.
    Otherwise, the ``out_dir``, ``name``, ``version`` and ``suffix`` are
    used to compose the target file path - the created archive file is
    ``[<out_dir>/]<name>[-<version>].tar`` (``[]`` means optional part and
    ``<>`` stands for argument substitution).  The target file extension might
    be changed with the ``suffix`` argument. The function also auto-generates
    the alias for this target, so user can build the archive with **scons
    <alias>**. To change the alias, provide an alternative with ``alias``
    argument. If you don't wish the alias to be created at all, set
    ``alias=None``.

    Certain leading paths can be stripped out from file names during package
    creation. These paths are provided with the ``strip_dirs`` argument.

    :Parameters:

        env
            the SCons Environment object
        name
            package name (string)
        source
            source files to be included in the archive

    :Keywords:
        alias
            SCons alias for this target, if not provided the default alias
            ``<name>-tar`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``
        alias_suffix
            alias suffix to be used instead of the default ``tar`` alias suffix
        out_dir
            output directory, where to create the archive
        strip_dirs
            directories to strip out from the paths of files in the archive,
            for example if ``source = ["sub1/foo.txt", "sub2/bar.txt",
            "sub3/geez.txt"]`` and ``strip_dirs = ["sub1", "sub3"]``, the
            resulting archive will contain files ``foo.txt``, ``sub2/bar.txt``
            and ``geez.txt``, you may also set ``strip_dirs=True`` to strip
            out the current working directory

        suffix
            suffix for the target file, by default the ``$TARSUFFIX``
            construction variable is used, or ``.tar`` if ``$TARSUFFIX`` is not
            set
        target
            target file name to use instead of the default auto-generated name
        version
            version of the package, used to generate the name of target file
    :Returns:
        a list of targets created (single target actually)
    """

    kw['default_alias_suffix'] = 'tar'
    kw['default_suffix'] = kw.get('TARFILESUFFIX',
                                  env.subst('$TARFILESUFFIX') or '.tar')
    return _tar(env, name, source, **kw)

def TarGz(env, name, source, **kw):
    """Create gzipped tar archive from source(s).

    This function creates gzipped TAR archive containing files listed in the
    ``source`` argument. The target file name may be fixed with the ``target``
    argument.  Otherwise, the ``out_dir``, ``name``, ``version`` and
    ``suffix`` are used to compose the target file path - the created archive
    file is ``[<out_dir>/]<name>[-<version>].tar.gz`` (``[]`` means optional
    part and ``<>`` stands for argument substitution).  The target file
    extension might be changed with the ``suffix`` argument. The function also
    auto-generates the alias for this target, so user can build the archive
    with **scons <alias>**. To change the alias, provide an alternative with
    ``alias`` argument. If you don't wish the alias to be created at all, set
    ``alias=None``.

    Certain leading paths can be stripped out from file names during package
    creation. These paths are provided with the ``strip_dirs`` argument.

    :Parameters:

        env
            the SCons Environment object
        name
            package name (string)
        source
            source files to be included in the archive

    :Keywords:
        alias
            SCons alias for this target, if not provided the default alias
            ``<name>-tgz`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``
        alias_suffix
            alias suffix to be used instead of the default ``tgz`` alias suffix
        out_dir
            output directory, where to create the archive
        strip_dirs
            directories to strip out from the paths of files in the archive,
            for example if ``source = ["sub1/foo.txt", "sub2/bar.txt",
            "sub3/geez.txt"]`` and ``strip_dirs = ["sub1", "sub3"]``, the
            resulting archive will contain files ``foo.txt``, ``sub2/bar.txt``
            and ``geez.txt``, you may also set ``strip_dirs=True`` to strip
            out the current working directory

        suffix
            suffix for the target file, by default ``.tar.gz`` is used
        target
            target file name to use instead of the default auto-generated name
        version
            version of the package, used to generate the name of target file
    :Returns:
        a list of targets created (single target actually)
    """

    kw['default_alias_suffix'] = 'tgz'
    kw['default_suffix'] = '.tar.gz'
    kw['TARFILEMODE'] = 'w:gz'
    return _tar(env, name, source, **kw)

def TarBz2(env, name, source, **kw):
    """Create bzipped tar archive from source(s).

    This function creates bzipped TAR archive containing files listed in the
    ``source`` argument. The target file name may be fixed with the ``target``
    argument.  Otherwise, the ``out_dir``, ``name``, ``version`` and
    ``suffix`` are used to compose the target file path - the created archive
    file is ``[<out_dir>/]<name>[-<version>].tar.bz2`` (``[]`` means optional
    part and ``<>`` stands for argument substitution).  The target file
    extension might be changed with the ``suffix`` argument. The function also
    auto-generates the alias for this target, so user can build the archive
    with **scons <alias>**. To change the alias, provide an alternative with
    ``alias`` argument. If you don't wish the alias to be created at all, set
    ``alias=None``.

    Certain leading paths can be stripped out from file names during package
    creation. These paths are provided with the ``strip_dirs`` argument.

    :Parameters:

        env
            the SCons Environment object
        name
            package name (string)
        source
            source files to be included in the archive

    :Keywords:
        alias
            SCons alias for this target, if not provided the default alias
            ``<name>-tbz2`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``
        alias_suffix
            alias suffix to be used instead of the default ``tbz2`` alias suffix
        out_dir
            output directory, where to create the archive
        strip_dirs
            directories to strip out from the paths of files in the archive,
            for example if ``source = ["sub1/foo.txt", "sub2/bar.txt",
            "sub3/geez.txt"]`` and ``strip_dirs = ["sub1", "sub3"]``, the
            resulting archive will contain files ``foo.txt``, ``sub2/bar.txt``
            and ``geez.txt``, you may also set ``strip_dirs=True`` to strip
            out the current working directory
        suffix
            suffix for the target file, by default ``.tar.bz2`` is used
        target
            target file name to use instead of the default auto-generated name
        version
            version of the package, used to generate the name of target file
    :Returns:
        a list of targets created (single target actually)
    """

    kw['default_alias_suffix'] = 'tbz2'
    kw['default_suffix'] = '.tar.bz2'
    kw['TARFILEMODE'] = 'w:bz2'
    return _tar(env, name, source, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
