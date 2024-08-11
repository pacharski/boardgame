print("BoardGame.board_game.test.setup.py")

import os
import sys
import pathlib

# organization is package/module/submodule
submodule = os.path.dirname(os.path.abspath(__file__))
module = os.path.dirname(submodule)
package = os.path.dirname(module)
sys.path.insert(0, package)

# sys.path.append('./model')
# print("SysPath", sys.path)

pathlib.Path('test/temp').mkdir(parents=True, exist_ok=True) 