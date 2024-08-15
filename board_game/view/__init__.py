import os
import sys

# organization is package/module/submodule
module = os.path.dirname(os.path.abspath(__file__))
package = os.path.dirname(module)
project = os.path.dirname(package)

sys.path.insert(0, project)
sys.path.insert(0, package)