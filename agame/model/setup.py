print("BoardGane.agame.model.setup")

import os
import sys

# organization is package/module/submodule
submodule = os.path.dirname(os.path.abspath(__file__))
module = os.path.dirname(submodule)
package = os.path.dirname(module)
sys.path.insert(0, package)