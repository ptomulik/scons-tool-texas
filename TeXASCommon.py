# -*- coding: utf-8 -*-
"""`TeXASCommon`

Utilities used commonly by other `texas` modules
"""
# -*- coding: utf-8 -*-

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

keywords = [
    'alias',
    'alias_suffix',
    'default_alias_suffix',
    'default_suffix',
    'out_dir',
    'suffix',
    'target',
    'version',
]

def RmDup(env, nodes, *args, **kw):
    """Remove duplicates from list ``nodes``, while preserving order"""
    result = []
    seen = set()
    nodes = env.arg2nodes(nodes, *args, **kw)
    for n in nodes:
        if not n in seen:
            result.append(n)
            seen.add(n)
    return result

def Children(env, node):
    node = env.arg2nodes(node, env.fs.Entry)[0]

    children = []
    def select_files(ss):
        import SCons.Node
        for s in ss:
            if isinstance(s, SCons.Node.FS.Dir):
                select_files(s.all_children())
            elif isinstance(s.disambiguate(), SCons.Node.FS.File):
                children.append(s)

    select_files(node.all_children())

    return RmDup(env, children)


def ImportFromTDS(env, source, **kw):
    """Import a file from TeX Directory Structure

    Use ``kpsewhich`` to search for source files within TeX Directory Structure
    (TDS) and copy them to the target directory ``out_dir``.

    Note: in addition to arguments documented here, this method accepts all
    keyword parameters recognized by ``env.KPSShowPath()`` and
    ``env.KPSFindFiles()``. See documentation of ``kpsewhich tool``.

    :Parameters:

        source
            (a list of) file(s) to be imported

    :Keywords:
        out_dir
            where to import files to, defaults to '.'

    :Returns:
        list of nodes created in the target directory.
    """
    import SCons.Util
    import SCons.Script
    import SCons.Errors
    import re
    import platform

    if not SCons.Util.is_Sequence(source): source = [source]
    source = [ env.subst(str(f)) for f in source ]

    try: out_dir = kw['out_dir']
    except KeyError: out_dir = env.Dir('.')

    found = {}
    for f in source:
        suffix = SCons.Util.silent_intern(SCons.Util.splitext(f)[1])
        if suffix:
            kw['path'] = env.KPSShowPath(suffix, **kw)
            # Remove all '.' (CWD) dir entries
            if platform.system() == 'Windows':
                kw['path'] = re.sub(r'(?:^\.[\\/]*;|;\.[\\/]*$)', r'', kw['path'])
                kw['path'] = re.sub(r';\.[\\/]*;',r';', kw['path'])
            else:
                kw['path'] = re.sub(r'(?:^\./*:|:\./*$)', r'', kw['path'])
                kw['path'] = re.sub(r':\./*:',r':', kw['path'])
            # Find the file in TDS
            found[f] = env.KPSFindFiles(f, **kw)
        else:
            raise SCons.Errors.UserError( "Can't import file '%s' " \
                                        + "which has no suffix." % f)
    target = []
    for dname, sname in found.items():
        dst = env.File(dname, out_dir)
        t = env.Command(dst, sname, SCons.Script.Copy('$TARGET', '$SOURCE'))
        target.extend(t)

    return target

def del_keys(dict_,keys):
    for k in keys:
        if k in dict_:
            del dict_[k]
    return dict_

def append_flags(env, key, flags, **kw):
    """Append new flags to ones existing in ``kw[key]`` or ``env[key]``.

    Return the "sum" of flags defined in ``kw[key]`` (or ``env[key]`` if the
    former is not set) and the ``flags``. If ``kw[key]`` is set, then the
    returned value is a "concatenation" of ``kw[key]`` and ``flags``, otherwise
    if ``env[key]`` is given, the function returns "concatenated" ``env[key]``
    and ``flags``. If none of ``kw[key]`` and ``env[key]`` is given, return
    ``flags``. The result is returned as an instance of ``SCons.Util.CLVar``
    object.

    :Parameters:
        env
            the SCons Environment object,
        key
            the keyword/construction variable holding the original flags,
        flags
            the extra flags to be appended to the original ones,
        kw
            keyword arguments, possibly with ``kw[key]`` set.

    :Returns:
        concatenated flags as ``SCons.Util.CLVar`` list.
    """
    import SCons.Util

    try:
        original = kw[key]
    except KeyError:
        try:
            original = env[key]
        except KeyError:
            original = []

    if SCons.Util.is_String(original):
        original = SCons.Util.CLVar([original])
    elif not isinstance(original, SCons.Util.CLVar):
        original = SCons.Util.CLVar(original)

    flags = original + SCons.Util.CLVar(flags)

    return flags

def get_auto_target(env, name, **kw):
    """Return an automatic target for some entity identified by ``name``.

    If the ``target``  keyword argument is set, return its value. Otherwise make
    and return a SCons Node object which points to a file
    ``[<out_dir>]/<name>[-version]<suffix>``. If ``suffix`` is not set, then
    ``default_suffix`` is used instead.

    :Parameters:

        env
            the SCons construction environment,
        name
            package name (string),

    :Keywords:

        suffix
            (optional) suffix for the target file,
        default_suffix
            default suffix for use when the ``suffix`` is not given,
        version
            (optional) package version,
        out_dir
            (optional) output directory for the target file,
        target
            (optional) the fixed target name to be returned instead of
            composing anything

    :Returns:
        target file as the ``SCons.Node.FS.File`` object (unless ``target``
        argument is provided and is not a Node)
    """
    import SCons.Node.FS
    try:
        target = kw['target']
    except KeyError:
        try:
            suffix = kw['suffix']
        except KeyError:
            try:
                suffix = kw['default_suffix']
            except KeyError:
                suffix = ''
        try:
            version = kw['version']
        except KeyError:
            version = None
        if version:
            target = '%s-%s%s' % (name, version, suffix)
        else:
            target = '%s%s' % (name, suffix)
        try:
            out_dir = kw['out_dir']
        except KeyError:
            out_dir = env.Dir('.')
        else:
            if not isinstance(out_dir, SCons.Node.FS.Dir):
                out_dir = env.Dir(out_dir)
        target = env.File(target, out_dir)

    return target

def get_auto_alias(name, alias_kw, **kw):
    """Return an automatic alias for some entity identified by ``name``.

    If the ``alias``  keyword argument is set, return its value. Otherwise
    compose and return an alias as ``<name>[-<alias_suffix>]``. If
    ``alias_suffix`` is not set, use ``default_alias_suffix`` instead.
    If neither of ``alias_suffix`` and ``default_alias_suffix`` is set,
    simply return ``name``.

    :Parameters:

        name
            package name (string),
        alias_kw
            base name of the keyword arguments holding alias information,
    :Keywords:

        alias_suffix
            (optional) suffix for the alias,
        default_alias_suffix
            default alias suffix, used when the ``suffix`` is not given,
        alias
            (optional) the fixed alias name to be returned instead of composing
            anything

    :Returns:
        an alias (string)
    """
    try:
        alias = kw[alias_kw]
    except KeyError:
        try:
            alias_suffix = kw['%s_suffix' % alias_kw]
        except KeyError:
            try:
                alias_suffix = kw['default_%s_suffix' % alias_kw]
            except KeyError:
                alias_suffix = None
        if alias_suffix:
            alias = '%s-%s' % (name, alias_suffix)
        else:
            alias = name
    return alias

def get_strip_dirs(env, **kw):
    """Prepare list of directory nodes to be stripped from the beginning of
    file names.

    :Parameters:
        env
            the SCons Environment object
    :Keywords:
        strip_dirs
            (optional) directory name (string) or sequence of
            directories (Nodes or strings) to be stripped out;
            if string is found, it is interpreted as a directory name
            relative to the current working directory,
    :Returns:
        list of paths (strings), each one relative to the top level source
        directory (denoted by '#' in SCons); if ``strip_dirs`` is not provided,
        an empty list is returned
    """
    import SCons.Util
    try:
        dirs = kw['strip_dirs']
    except KeyError:
        dirs = []

    if SCons.Util.is_String(dirs):
        dirs = [ env.Dir(dirs) ]
    elif SCons.Util.is_Sequence(dirs):
        dirs = [ env.Dir(d) for d in dirs ]
    elif dirs:
        dirs = [ env.Dir('.') ]
    else:
        dirs = []

    dirs2 = dirs[:]
    for d in dirs:
        s = d.srcnode()
        if d != s:
            dirs2.append(s)
    return dirs2

def joinpathre(dirs):
    import re
    import platform
    paths = [ str(d) for d in dirs ]
    # Escape the paths for sed regular expression
    paths = [ re.sub(r'([\.\[\]:\*])', r'\\\1', p) for p in paths ]
    paths = [ re.sub(r'\/*$', r'/*', p) for p in paths ]
    if platform.system() == 'Windows':
        paths = [ re.sub(r'([&<>|\'`,;=()!^])', r'^\1', p) for p in paths ]
        return '\\^|'.join(paths)
    else:
        return '\\|'.join(paths)

def posixsep(node):
    import SCons.Util
    import os
    def ts(n): return '/'.join(n.split(os.path.sep))
    if SCons.Util.is_List(node):
        return [ts(str(n)) for n in node]
    else:
        return ts(str(node))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
