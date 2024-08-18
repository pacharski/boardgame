# To run unit tests from boardgame directory, Run with:
#     'python a_game'

from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

print("Run a_game unittests")

import unittest
import os

here = os.path.dirname(os.path.abspath(__file__))
testsuite = unittest.TestLoader().discover(here)

# 0 (quiet): you just get the total numbers of tests executed and the global result
# 1 (default): you get the same plus a dot for every successful test or a F for every failure
# 2 (verbose): you get the help string of every test and the result
unittest.TextTestRunner(verbosity=1).run(testsuite)
