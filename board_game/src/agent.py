# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
import random

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import board_game as bg


class Agent(): 
    def __init__(self, player: bg.Player, board: bg.Board):
        self.player = player
        self.board = board

    def turn(self):
        move_count = random.randint(0, 5)
        action_count = 1
        while action_count > 0:
            if action_count <= move_count:
                action = self.move()
                yield action
                action_count += 1
            else:
                action_count = 0

    def take_turn(self):
        self.move()

    def move(self):
        count = random.randint(0, 5)
        for _ in range(count):
            exits = self.board.spaces[self.player.location].exits
            if (exits != None) and (len(exits) > 0):
                exit = exits[random.randint(1, len(exits)) - 1]
                from_location = self.player.location
                self.player.location = exit.destination 
                return ("Move", from_location, exit.barrier, self.player.location)

    
if __name__ == "__main__":
    import os
    import sys
    p = bg.Player("Scooby", "Brown Dog", location=93, id=0)
    here = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(here, "../../data/board.json")
    b = bg.Board(json_path=json_path)
    #b.save_to_json_path("newboard.json")
    a = Agent(p, b)

    for action in a.turn():
        print("Action", action)
    