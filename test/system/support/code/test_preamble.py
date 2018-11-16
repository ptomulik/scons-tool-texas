import TestSCons
import sys

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()


test.dir_fixture('image')
test.subdir(['site_scons'])
test.subdir(['site_scons', 'site_tools'])
test.subdir(['site_scons', 'site_tools', 'texas'])
for f in ('about.py', '__init__.py', 'TeXASCommon.py', 'TeXASDist.py', 'TeXASDoc.py'):
    test.file_fixture('../../../../../../%s' % f, 'site_scons/site_tools/texas/%s' % f)
test.subdir(['site_scons', 'site_tools', 'ci'])
test.file_fixture('../../../../support/ci/__init__.py', 'site_scons/site_tools/ci/__init__.py')
