import setup
import unittest

loader = unittest.TestLoader()
testSuite = loader.discover('.')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)