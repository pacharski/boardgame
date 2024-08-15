print("BoardGane.board_game.model.setup")

import os
import sys

# organization is project/package/module
module = os.path.dirname(os.path.abspath(__file__))
package = os.path.dirname(module)
project = os.path.dirname(package)

sys.path.insert(0, package)
sys.path.insert(0, project)
#sys.path.insert(0, module)