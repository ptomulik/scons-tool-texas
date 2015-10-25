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

"""
TODO: Write documentation
"""

import TestSCons

test = TestSCons.TestSCons()

test.dir_fixture('image')
test.dir_fixture('../../../../texas', 'src/site_scons/site_tools/texas')
test.file_fixture('../../../../site_scons/site_tools/kpsewhich.py', 'src/site_scons/site_tools/kpsewhich.py')

test.subdir(['share'])
test.subdir(['share', 'texmf'])
test.subdir(['share', 'texmf', 'tex'])
test.subdir(['share', 'texmf', 'tex', 'latex'])
test.subdir(['share', 'texmf', 'tex', 'latex', 'local'])
test.subdir(['share', 'texmf', 'bibtex'])
test.subdir(['share', 'texmf', 'bibtex', 'bib'])
test.subdir(['share', 'texmf', 'bibtex', 'bib', 'local'])

test.write( ['share', 'texmf', 'tex', 'latex', 'local', 'foo.cls'],
            "orig-foo.cls" )
test.write( ['share', 'texmf', 'bibtex', 'bib', 'local', 'foo.bib'],
            "orig-foo.bib" )

# Normal invocation
test.run(chdir = 'src')
test.must_exist(test.workpath('src/foo.cls'))
test.must_exist(test.workpath('src/foo.bib'))
test.write('src/foo.cls', 'orig-foo.cls')
test.must_contain('src/foo.cls', "rig-foo.cls")
test.must_contain('src/foo.bib', "rig-foo.bib")

#
# Ensure that TeXASImport() is not fooled by files existing locally
test.write( ['share', 'texmf', 'tex', 'latex', 'local', 'foo.cls'],
            "updated-foo.cls" )
test.write( ['share', 'texmf', 'bibtex', 'bib', 'local', 'foo.bib'],
            "updated-foo.bib" )
test.run(chdir = 'src')
test.must_exist(test.workpath('src/foo.cls'))
test.must_exist(test.workpath('src/foo.bib'))
test.must_contain('src/foo.cls', 'pdated-foo.cls')
test.must_contain('src/foo.bib', 'pdated-foo.bib')

# Cleanup
test.run(arguments=['-c'], chdir = 'src')
test.must_not_exist(test.workpath('src/foo.cls'))
test.must_not_exist(test.workpath('src/foo.bib'))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
