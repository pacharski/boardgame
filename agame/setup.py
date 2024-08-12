print("BoardGame.agame.setup")

import os
import sys

# organization is project/package/module/submodule
module = os.path.dirname(os.path.abspath(__file__))
package = os.path.dirname(module)
sys.path.insert(0, package)