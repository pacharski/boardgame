print("BoardGame.board_game.setup")

import os
import sys

# organization is package/module/submodule
module = os.path.dirname(os.path.abspath(__file__))
package = os.path.dirname(module)
sys.path.insert(0, package)