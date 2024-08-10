# To run unit tests from boardgame directory, Run with:
#     'python boardgame'

import os
print("Run boardgame unittests", os.getcwd())

import unittest

testsuite = unittest.TestLoader().discover('.')
print(testsuite)
unittest.TextTestRunner(verbosity=1).run(testsuite)