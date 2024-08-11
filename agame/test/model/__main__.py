import os
import sys
import unittest

print("test.__main__.py", os.getcwd())
sys.path.append('./model')
print("SysPath", sys.path)

loader = unittest.TestLoader()
testSuite = loader.discover('.')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)
