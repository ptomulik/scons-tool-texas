"""`TeXASCommon`

Utilities used commonly by other `texas` modules
"""

#
# Copyright (c) 2013 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>
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

    :Arguments:
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

def get_auto_alias(name, **kw):
    """Return an automatic alias for some entity identified by ``name``.
    
    If the ``alias``  keyword argument is set, return its value. Otherwise
    compose and return an alias as ``<name>[-<alias_suffix>]``. If
    ``alias_suffix`` is not set, use ``default_alias_suffix`` instead.
    If neither of ``alias_suffix`` and ``default_alias_suffix`` is set,
    simply return ``name``.

    :Parameters:

        name
            package name (string),

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
        alias = kw['alias']
    except KeyError:
        try:
            alias_suffix = kw['alias_suffix']
        except KeyError: 
            try: 
                alias_suffix = kw['default_alias_suffix']
            except KeyError:
                alias_suffix = None
        if alias_suffix: 
            alias = '%s-%s' % (name, alias_suffix)
        else:
            alias = name
    return alias

def get_strip_paths(env, **kw):
    """Prepare list of paths to strip from the beginning of file names.
    
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

    top = env.Dir('#')

    if SCons.Util.is_String(dirs):
        dirs = [ env.Dir(dirs) ]
    elif SCons.Util.is_Sequence(dirs):
        dirs = [ env.Dir(d) for d in dirs ]
    elif dirs:
        dirs = [ env.Dir('.') ]
    else: 
        paths = []
     
    dirs2 = dirs[:]
    for d in dirs:
        s = d.srcnode()
        if d != s:
            dirs2.append(s)

    paths = [ top.rel_path(d) for d in list(set(dirs2)) ]
    return paths 

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4: