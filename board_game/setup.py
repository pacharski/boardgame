print("BoardGame.board_game.setup")

import os
import sys

# organization is project/package/module/submodule
# board_game is a package
package = os.path.dirname(os.path.abspath(__file__))
project = os.path.dirname(package)
sys.path.insert(0, project)