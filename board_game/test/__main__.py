import os
import sys
import pathlib

import unittest

print("test.__main__.py", os.getcwd())
sys.path.append('./model')
print("SysPath", sys.path)

pathlib.Path('model/temp').mkdir(parents=True, exist_ok=True) 

loader = unittest.TestLoader()
testSuite = loader.discover('.')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)