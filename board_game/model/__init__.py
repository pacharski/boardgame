import sys
import os
sys.path.append('../model')               # so tests will find model
sys.path.append('./board_game/model')     # so view will find model
print("model.__init__", os.getcwd())