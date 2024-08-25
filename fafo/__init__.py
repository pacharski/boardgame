from pathlib import Path 
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here)

from fafo.src.game import Game
from fafo.src.game_view import GameView
from fafo.src.table_view import TableView