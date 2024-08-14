print("BoardGame.board_game.test.setup.py")

import os
import sys
import pathlib

# organization is package/module/submodule
submodule = os.path.dirname(os.path.abspath(__file__))
module = os.path.dirname(submodule)
package = os.path.dirname(module)
project = os.path.dirname(package)
sys.path.insert(0, project) 

# use this to create directories that may be needed if they don't exist
#pathlib.Path('test/temp').mkdir(parents=True, exist_ok=True) 