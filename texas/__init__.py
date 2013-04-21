"""`texas`
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

import SCons.Tool.dvipdf
import SCons.Tool.latex
import SCons.Tool.pdflatex
import SCons.Tool.pdftex
import SCons.Tool.tar
import SCons.Tool.tex
import TeXASDist
import TeXASDoc

_tar_generated = False
_dvi_generated = False
_pdf_generated = False
_dvipdfm_generated = False

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

def _generate_tar(env):
    global _tar_generated
    if not _tar_generated:
        if SCons.Tool.tar.exists(env):
            SCons.Tool.tar.generate(env)
            _tar_generated = True
        if _tar_generated:
            env.AddMethod(TeXASDist.Tar, 'TeXASTar') 
            env.AddMethod(TeXASDist.TarGz, 'TeXASTarGz') 
            env.AddMethod(TeXASDist.TarBz2, 'TeXASTarBz2') 

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
        try: env.Tool('dvipdfm')
        except SCons.Errors.EnvironmentError: return
        else:
            env.AddMethod(TeXASDoc.DVIPDFM, 'TeXASDVIPDFM')
            # fix for the problem with out_dir
            env['TEXASDVIPDFMCOM'] = 'cd ${TARGET.dir} && ' \
                + '$DVIPDFM $DVIPDFMFLAGS -o ${TARGET.file} ' \
                + '${TARGET.rel_path(SOURCE)}'
            _dvipdfm_generated = True
    

def generate(env):
    _generate_tar(env)
    _generate_dvi(env)
    _generate_pdf(env)
    _generate_dvipdfm(env)
    env.AddMethod(TeXASDoc.Doc, 'TeXASDoc')
    env.AddMethod(RmDup, 'TeXASRmDup')

def exists(env):
    SCons.Tool.tex.generate_darvin(env)
    return SCons.tar.exists(env) and SCons.dvipdf.exists(env) and \
           (SCons.pdftex.exists(env) or SCons.pdflatex.exists(env)) and \
           (SCons.latex.exists(env) or SCons.tex.exists(env))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
