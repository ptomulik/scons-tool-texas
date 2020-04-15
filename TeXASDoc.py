# -*- coding: utf-8 -*-
"""`TeXASDoc`

Utilities for the compilation of LaTeX papers (articles).
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

class _Null(object): pass
_null = _Null

_local_keywords = TeXASCommon.keywords  + [
    'deps',
    'builder'
]

def _del_local_keywords(kw):
    global _local_keywords
    return TeXASCommon.del_keys(kw, _local_keywords)

def _builddoc(env, name, source=_null, **kw):
    import SCons.Errors
    try: builder = kw['builder']
    except KeyError: builder = 'DVI'

    if builder == 'DVI' and 'suffix' in kw: del kw['suffix']
    if source is _null: source = name

    alias = TeXASCommon.get_auto_alias(name, 'alias', **kw)
    target = TeXASCommon.get_auto_target(env, name, **kw)

    try: deps = kw['deps']
    except KeyError: deps = None

    kw = _del_local_keywords(kw)

    if builder == 'DVI':
        target = env.DVI(target, source, **kw)
        if deps: env.Depends(target, deps)
    elif builder == 'PDF':
        try: kw['DVIPDFCOM'] = env['TEXASDVIPDFCOM']
        except KeyError: pass
        target = env.PDF(target, source, **kw)
        if deps: env.Depends(target, deps)
    elif builder == 'DVIPDFM':
        try: kw['DVIPDFMCOM'] = env['TEXASDVIPDFMCOM']
        except KeyError: pass
        target = env.DVIPDFM(target, source, **kw)
        if deps: env.Depends(target, deps)
    else:
        raise SCons.Errors.UserError('Unsupported builder: %r' % builder)
    if alias:
        env.Alias(alias, target)
        env.AlwaysBuild(alias)
    return target

def Doc(env, name, source=_null, **kw):
    """Compile document in one of the supported formats

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
            ``<name>-dvi`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``,
        alias_suffix
            alias suffix to be used instead of the default ``dvi`` alias suffix,
        builder
            string - name of the builder used to create target, currently
            supported values are ``'DVI'``, ``'PDF'`` and ``'DVIPDFM'``,
        deps
            extra dependencies for target file
        out_dir
            output directory
        suffix
            ignored, the suffix is hard-coded to ``.dvi``
        target
            target file name to use instead of the default auto-generated name,
        version
            used to generate target name,
    :Returns:
        a list of targets created (single target actually)
    """
    import SCons.Errors
    if 'builder' not in kw:
        kw['builder'] = 'DVI'

    if kw['builder'] == 'DVI':
        # Suffixes are fixed for DVI builder
        kw['default_alias_suffix'] = 'dvi'
        kw['default_suffix'] = '.dvi'
    elif kw['builder'] == 'PDF':
        kw['default_alias_suffix'] = 'pdf'
        try: kw['default_suffix'] = kw['PDFSUFFIX']
        except KeyError:
            kw['default_suffix'] = env.subst('$PDFSUFFIX')
            if not kw['default_suffix']:
                kw['default_suffix'] = '.pdf'
    elif kw['builder'] == 'DVIPDFM':
        kw['default_alias_suffix'] = 'pdf'
        try: kw['default_suffix'] = kw['DVIPDFMSUFFIX']
        except KeyError:
            kw['default_suffix'] = env.subst('$DVIPDFMSUFFIX')
            if not kw['default_suffix']:
                kw['default_suffix'] = '.pdf'
    else:
        raise SCons.Errors.UserError('Unsupported builder: %r' % repr(kw['builder']))

    return _builddoc(env, name, source, **kw)

def DVI(env, name, source=_null, **kw):
    """Compile ``*.dvi`` document with SCons DVI builder.

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
            ``<name>-dvi`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``,
        alias_suffix
            alias suffix to be used instead of the default ``dvi`` alias suffix,
        deps
            extra dependencies for DVI target,
        out_dir
            output directory
        suffix
            ignored, the suffix is hard-coded to ``.dvi``
        target
            target file name to use instead of the default auto-generated name,
        version
            used to generate target name,

    :Returns:
        a list of targets created (single target actually)
    """
    kw['builder'] = 'DVI'
    return Doc(env, name, source, **kw)

def PDF(env, name, source=_null, **kw):
    """Compile ``*.pdf`` document with SCons PDF builder.

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
            ``<name>-dvi`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``,
        alias_suffix
            alias suffix to be used instead of the default ``dvi`` alias suffix,
        deps
            extra dependencies for PDF target,
        out_dir
            output directory
        suffix
            suffix for the target file, by default the ``$PDFSUFFIX``
            construction variable is used, or ``.pdf`` if ``$PDFSUFFIX`` is not
            set
        target
            target file name to use instead of the default auto-generated name,
        version
            used to generate target name,
    :Returns:
        a list of targets created (single target actually)
    """
    kw['builder'] = 'PDF'
    return Doc(env, name, source, **kw)

def DVIPDFM(env, name, source=_null, **kw):
    """Compile ``*.pdf`` document with SCons DVIPDFM builder.

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
            ``<name>-dvi`` or ``<name>-<alias_suffix>`` is used,
            otherwise the alias is set to the value of this argument; to not
            create any alias set ``alias=None``,
        alias_suffix
            alias suffix to be used instead of the default ``dvi`` alias suffix,
        deps
            extra dependencies for PDF target,
        out_dir
            output directory
        suffix
            suffix for the target file, by default the ``$DVIPDFMSUFFIX``
            construction variable is used, or ``.pdf`` if ``$DVIPDFMSUFFIX`` is
            not set
        target
            target file name to use instead of the default auto-generated name,
        version
            used to generate target name,

    :Returns:
        a list of targets created (single target actually)
    """
    kw['builder'] = 'DVIPDFM'
    return Doc(env, name, source, **kw)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
