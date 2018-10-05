#! /usr/bin/env python

#
# Copyright (c) 2015 by Pawel Tomulik
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

# Download local stuff required to generate docs and/or run test suites

import argparse
import os
import sys
import tarfile
import re
import io
import shutil

try:
    # Python 3
    from urllib.request import urlopen, urlretrieve
except ImportError:
    # Python 2
    from urllib2 import urlopen
    from urllib import urlretrieve

def scons_version_string(s):
    if not s in _scons_versions:
        supported = ', '.join(["'%s'" % v for v in  _scons_versions])
        raise argparse.ArgumentTypeError('wrong version %r, supported versions are: %s' % (s, supported))
    return s

def scons_test_version_string(s):
    if not s in _scons_test_versions:
        supported = ', '.join(["'%s'" % v for v in  _scons_test_versions])
        raise argparse.ArgumentTypeError('wrong version %r, supported versions are: %s' % (s, supported))
    return s

def scons_docbook_version_string(s):
    if not s in _scons_docbook_versions:
        supported = ', '.join(["'%s'" % v for v in  _scons_docbook_versions])
        raise argparse.ArgumentTypeError('wrong version %r, supported versions are: %s' % (s, supported))
    return s

def scons_dvipdfm_version_string(s):
    if not s in _scons_dvipdfm_versions:
        supported = ', '.join(["'%s'" % v for v in  _scons_dvipdfm_versions])
        raise argparse.ArgumentTypeError('wrong version %r, supported versions are: %s' % (s, supported))
    return s

def scons_kpsewhich_version_string(s):
    if not s in _scons_kpsewhich_versions:
        supported = ', '.join(["'%s'" % v for v in  _scons_kpsewhich_versions])
        raise argparse.ArgumentTypeError('wrong version %r, supported versions are: %s' % (s, supported))
    return s

def untar(tar, **kw):
    # Options
    try:                strip_components = kw['strip_components']
    except KeyError:    strip_components = 0
    try:                member_name_filter = kw['member_name_filter']
    except KeyError:    member_name_filter = lambda x : True
    try:                path = kw['path']
    except KeyError:    path = '.'
    # Download the tar file
    members = [m for m in tar.getmembers() if len(m.name.split('/')) > strip_components]
    if strip_components > 0:
        for m in members:
            m.name = '/'.join(m.name.split('/')[strip_components:])

    members = [m for m in members if member_name_filter(m.name) ]
    tar.extractall(path = path, members = members)

def urluntar(url, **kw):
    # Download the tar file
    tar = tarfile.open(fileobj = io.BytesIO(urlopen(url).read()))
    untar(tar, **kw)
    tar.close()

def info(msg, **kw):
    try: quiet = kw['quiet']
    except KeyError: quiet = False
    if not quiet:
        sys.stdout.write("%s: info: %s\n" % (_script, msg))

def warn(msg, **kw):
    try: quiet = kw['quiet']
    except KeyError: quiet = False
    if not quiet:
        sys.stderr.write("%s: warning: %s\n" % (_script, msg))
    untar(tar, **kw)
    tar.close()

def dload_scons_test(**kw):
    try: ver = kw['scons_test_version']
    except KeyError:
        try: ver = kw['scons_version']
        except KeyError: ver = _default_scons_test_version

    clean = False
    try: clean = kw['clean']
    except KeyError: pass

    destdir = _topsrcdir

    if clean:
        info("cleaning scons-test", **kw)
        for f in ['runtest.py', 'testing']:
            ff = os.path.join(destdir,f)
            if os.path.exists(ff):
                info("removing '%s'" % ff, **kw)
                if os.path.isdir(ff):
                    shutil.rmtree(ff)
                else:
                    os.remove(ff)
        return 0

    url = "https://github.com/scons/scons/archive/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    member_name_filter = lambda s : re.match('(?:^runtest\.py$|testing/)', s)
    urluntar(url, path = destdir, strip_components = 1, member_name_filter = member_name_filter)
    return 0

def dload_scons_docbook(**kw):
    try: ver = kw['scons_docbook_version']
    except KeyError: ver = _default_scons_docbook_version

    clean = False
    try: clean = kw['clean']
    except KeyError: pass

    destdir = os.path.join(_topsrcdir, 'site_scons', 'site_tools', 'docbook')

    if clean:
        info("cleaning scons-docbook", **kw)
        if os.path.exists(destdir):
            info("removing '%s'" % destdir, **kw)
            shutil.rmtree(destdir)
        return 0

    if not os.path.exists(destdir):
        info("creating '%s'" % destdir, **kw)
        os.makedirs(destdir)

    url = "https://bitbucket.org/dirkbaechle/scons_docbook/get/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    member_name_filter = lambda s : re.match('(?:^__init__\.py$|utils/|docbook-xsl-[^/]+/)', s)
    urluntar(url, path = destdir, strip_components = 1, member_name_filter = member_name_filter)
    return 0

def dload_scons_dvipdfm(**kw):
    try: ver = kw['scons_dvipdfm_version']
    except KeyError: ver = _default_scons_dvipdfm_version

    clean = False
    try: clean = kw['clean']
    except KeyError: pass

    destdir = os.path.join(_topsrcdir, 'site_scons', 'site_tools')

    if clean:
        info("cleaning scons-dvipdfm", **kw)
        content = ['dvipdfm.py']
        for f in content:
            ff = os.path.join(destdir, f)
            if os.path.exists(ff):
                info("removing '%s'" % ff, **kw)
                if os.path.isdir(ff):
                    shutil.rmtree(ff)
                else:
                    os.remove(ff)
        return 0

    if not os.path.exists(destdir):
        info("creating '%s'" % destdir, **kw)
        os.makedirs(destdir)

    url = "https://github.com/ptomulik/scons-tool-dvipdfm/archive/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    member_name_filter = lambda s : re.match('(?:^dvipdfm.py$)', s)
    urluntar(url, path = destdir, strip_components = 1, member_name_filter = member_name_filter)
    return 0

def dload_scons_kpsewhich(**kw):
    try: ver = kw['scons_kpsewhich_version']
    except KeyError: ver = _default_scons_kpsewhich_version

    clean = False
    try: clean = kw['clean']
    except KeyError: pass

    destdir = os.path.join(_topsrcdir, 'site_scons', 'site_tools')

    if clean:
        info("cleaning scons-kpsewhich", **kw)
        content = ['kpsewhich']
        for f in content:
            ff = os.path.join(destdir, f)
            if os.path.exists(ff):
                info("removing '%s'" % ff, **kw)
                if os.path.isdir(ff):
                    shutil.rmtree(ff)
                else:
                    os.remove(ff)
        return 0

    if not os.path.exists(destdir):
        info("creating '%s'" % destdir, **kw)
        os.makedirs(destdir)

    url = "https://github.com/ptomulik/scons-tool-kpsewhich/archive/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    member_name_filter = lambda s : re.match(r'(?:^kpsewhich/)', s)
    urluntar(url, path = destdir, strip_components = 1, member_name_filter = member_name_filter)
    return 0

# The script...
_script = os.path.basename(sys.argv[0])
_scriptabs = os.path.realpath(sys.argv[0])
_scriptdir = os.path.dirname(_scriptabs)
_topsrcdir = os.path.realpath(os.path.join(_scriptdir, '..'))

_all_packages = [ 'scons-test',
                  'scons-docbook',
                  'scons-dvipdfm',
                  'scons-kpsewhich',
                ]

_default_packages = [ 'scons-test',
                      'scons-dvipdfm',
                      'scons-kpsewhich',
                    ]

# scons
_scons_versions = ['master',
                   '3.0.1',
                   '3.0.0',
                   '2.5.1',
                   '2.5.0',
                   '2.4.1',
                   '2.4.0',
                   '2.3.6',
                   '2.3.5',
                   '2.3.4',
                   '2.3.3',
                   '2.3.2',
                   '2.3.1',
                   '2.3.0',
                   '2.2.0',
                   '2.1.0.final.0' ]
_default_scons_version = _scons_versions[0]

# scons-test
_scons_test_versions = _scons_versions
_default_scons_test_version = _scons_test_versions[0]

# scons-docbook
_scons_docbook_versions = [ 'tip' ]
_default_scons_docbook_version = _scons_docbook_versions[0]

# scons-dvipdfm
_scons_dvipdfm_versions = [ 'master' ]
_default_scons_dvipdfm_version = _scons_dvipdfm_versions[0]

# scons-kpsewhich
_scons_kpsewhich_versions = [ 'master' ]
_default_scons_kpsewhich_version = _scons_kpsewhich_versions[0]

_parser = argparse.ArgumentParser(
        prog=_script,
        description="""\
        This tool downloads predefined prerequisites for the scons-tool-texas
        project. You may cherry pick what to download or simply download all
        (if you don't specify explicitly packages, all predefined packages are
        being downloaded). The downloaded stuff is placed in predefined
        subdirectories of the source tree such that they are later found
        automatically when the project is being built.
        """)

_parser.add_argument('--quiet',
                      action='store_true',
                      help='do not print messages')
_parser.add_argument('--clean',
                      action='store_true',
                      help='clean downloaded package(s)')
_parser.add_argument('--scons-version',
                      type=scons_version_string,
                      default=_default_scons_version,
                      metavar='VER',
                      help='version of SCons to be downloaded')
_parser.add_argument('--scons-test-version',
                      type=scons_test_version_string,
                      default=_default_scons_test_version,
                      metavar='VER',
                      help='version of SCons test framework to be downloaded')
_parser.add_argument('--scons-docbook-version',
                      type=scons_docbook_version_string,
                      default=_default_scons_docbook_version,
                      metavar='VER',
                      help='version of SCons docbook tool to be downloaded')
_parser.add_argument('--scons-dvipdfm-version',
                      type=scons_dvipdfm_version_string,
                      default=_default_scons_dvipdfm_version,
                      metavar='VER',
                      help='version of SCons dvipdfm tool to be downloaded')
_parser.add_argument('--scons-kpsewhich-version',
                      type=scons_kpsewhich_version_string,
                      default=_default_scons_kpsewhich_version,
                      metavar='VER',
                      help='version of SCons kpsewhich tool to be downloaded')
_parser.add_argument('packages',
                      metavar='PKG',
                      type=str,
                      nargs='*',
                      default = _default_packages,
                      help='package to download (%s)' % ', '.join(_all_packages))

_args = _parser.parse_args()

for pkg in _args.packages:
    if pkg.lower() == 'scons-test':
        dload_scons_test(**vars(_args))
    elif pkg.lower() == 'scons-docbook':
        dload_scons_docbook(**vars(_args))
    elif pkg.lower() == 'scons-dvipdfm':
        dload_scons_dvipdfm(**vars(_args))
    elif pkg.lower() == 'scons-kpsewhich':
        dload_scons_kpsewhich(**vars(_args))
    else:
        warn("unsupported package: %r")

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
