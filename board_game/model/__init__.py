from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

# import all of the separate files so they will be treated as one module
from . import point, space, path, exit, board, jsoninator
from . import card, marker, player, hoard, horde
