# -*- coding: utf-8 -*-
"""`texas`
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

from .about import __version__

import SCons.Tool.dvipdf
import SCons.Tool.latex
import SCons.Tool.pdflatex
import SCons.Tool.pdftex
import SCons.Tool.tex

from . import TeXASDist
from . import TeXASDoc

try:
    import site_tools.dvipdfm as dvipdfm
except ImportError:
    import sconstool.dvipdfm as dvipdfm

try:
    import site_tools.kpsewhich as kpsewhich
except ImportError:
    import sconstool.kpsewhich as kpsewhich

try:
    import site_tools.archives as archives
except ImportError:
    import sconstool.archives as archives

_archives_generated = False
_dvi_generated = False
_pdf_generated = False
_dvipdfm_generated = False
_kpsewhich_generated = False

def _generate_archives(env):
    global _archives_generated
    if not _archives_generated:
        archives.generate(env)
        env.AddMethod(TeXASDist.Tar, 'TeXASTar')
        env.AddMethod(TeXASDist.TarGz, 'TeXASTarGz')
        env.AddMethod(TeXASDist.TarBz2, 'TeXASTarBz2')
        _archives_generated = True

def _generate_dvi(env):
    global _dvi_generated
    if not _dvi_generated:
        if SCons.Tool.tex.exists(env):
            SCons.Tool.tex.generate(env)
            _dvi_generated = True
        if SCons.Tool.latex.exists(env):
            SCons.Tool.latex.generate(env)
            _dvi_generated = True
        if _dvi_generated:
            env.AddMethod(TeXASDoc.DVI, 'TeXASDVI')

def _generate_pdf(env):
    global _pdf_generated
    if not _pdf_generated:
        if SCons.Tool.dvipdf.exists(env):
            SCons.Tool.dvipdf.generate(env)
            # fix for the problem with out_dir
            env['TEXASDVIPDFCOM'] = 'cd ${TARGET.dir} && ' \
              + '$DVIPDF $DVIPDFFLAGS ${TARGET.rel_path(SOURCE)} ' \
              + '${TARGET.file}'
            _pdf_generated = True
        if SCons.Tool.pdftex.exists(env):
            SCons.Tool.pdftex.generate(env)
            _pdf_generated = True
        if SCons.Tool.pdflatex.exists(env):
            SCons.Tool.pdflatex.generate(env)
            _pdf_generated = True
        if _pdf_generated:
            env.AddMethod(TeXASDoc.PDF, 'TeXASPDF')

def _generate_dvipdfm(env):
    import SCons.Errors
    global _dvipdfm_generated
    if not _dvipdfm_generated:
        dvipdfm.generate(env)
        env.AddMethod(TeXASDoc.DVIPDFM, 'TeXASDVIPDFM')
        # fix for the problem with out_dir
        env['TEXASDVIPDFMCOM'] = 'cd ${TARGET.dir} && ' \
            + '$DVIPDFM $DVIPDFMFLAGS -o ${TARGET.file} ' \
            + '${TARGET.rel_path(SOURCE)}'
        _dvipdfm_generated = True

def _generate_kpsewhich(env):
    import SCons.Errors
    global _kpsewhich_generated
    if not _kpsewhich_generated:
        kpsewhich.generate(env)
        env.AddMethod(TeXASCommon.ImportFromTDS, 'TeXASImport')
        _kpsewhich_generated = True


def generate(env):
    _generate_archives(env)
    _generate_dvi(env)
    _generate_pdf(env)
    _generate_dvipdfm(env)
    _generate_kpsewhich(env)
    env.AddMethod(TeXASDoc.Doc, 'TeXASDoc')
    env.AddMethod(TeXASCommon.RmDup, 'TeXASRmDup')
    env.AddMethod(TeXASCommon.Children, 'TeXASChildren')

def exists(env):
    SCons.Tool.tex.generate_darvin(env)
    return SCons.dvipdf.exists(env) and \
           (SCons.pdftex.exists(env) or SCons.pdflatex.exists(env)) and \
           (SCons.latex.exists(env) or SCons.tex.exists(env) and \
           dvipdfm.exists(env) and kpsewhich.exists(env) and \
           archives.exists(env))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
