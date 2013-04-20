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
import tarfile

alias = 'package-tar'
tarname = 'package.tar'
srcfiles = sorted(['geez.txt', 'sub1/foo.txt', 'sub1/sub2/bar.txt'])

test = TestSCons.TestSCons()

test.dir_fixture('image')
test.dir_fixture('../../../../texas', 'site_scons/site_tools/texas')

# Normal invocation
test.run(arguments = alias)
test.must_exist(test.workpath(tarname))

tar = tarfile.open(tarname, 'r')
tarfiles = sorted(tar.getnames())
if not (srcfiles == tarfiles):
    print "The archive %s should contain following files: " \
        % test.workpath(tarname)
    print '  ' + str(srcfiles)
    print "but it contains:" 
    print '  ' + str(tarfiles)
    test.fail_test()

# Cleanup
test.run(arguments=['-c', alias])
test.must_not_exist(test.workpath(tarname))

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4: