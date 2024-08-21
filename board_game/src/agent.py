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
    def __init__(self, player: bg.Player, board: bg.Board, players: list):
        self.player = player
        self.board = board
        self.players = players

    def turn(self):
        action_list = self.move(5)
        if action_list != None:
            for action in action_list:
                yield action
        
    def move(self, max_moves=None):
        """ figure out the possible move options for the player, and pick one"""
        max_moves = max_moves if (max_moves != None) else 5
        for move_count in range(max_moves):
            """
                Use all the moves to be a valid option or end at an encounter
                Do not end in space with another player unless it is a big room to be valid
                Ending on a space with an unknown secret door without a monster to fight, allows
                 searching for the secret door
            """
            valid_options = self.search_moves(self.player, self.player.location, None, move_count, [], [])
        if len(valid_options) > 1:
            select = random.randint(1, len(valid_options))
            return valid_options[select-1]
        elif len(valid_options) > 0:
            return valid_options[0]
        # default to return None (should never happen, could always stay where you are)

    def is_encounter(self, location):
        space = self.board.spaces[location]
        if ((space.name == "") or (location == 92) or (location == 93)):
            return False
        elif (space.name == "Room"):
            if space.num_encounters == 0:
                return True
            adversary, rewards, assigned = space.encounters[0]
            return (adversary != None)
        else: # big room
            return True
    
    def is_occupied(self, location):
        # exclude self.player
        occupied_locations = [player.location for player in self.players if player != self.player]
        return location in occupied_locations

    def search_moves(self, player, location, last_exit, count, option, valid_options):
        """recursive search to create a list of valid move options"""
        encounter = (len(option) != 0) and self.is_encounter(location) # check board state
        occupied = self.is_occupied(location) # check board state, exclude self.player
        # if no more movement left, done moving
        if count == 0:
            if not occupied:
                # check for secret doors
                space = self.board.spaces[location]
                secret_doors = [exit for exit in space.exits if exit.barrier == "Secret Door"]
                if len(secret_doors) > 0:
                    secret_door = random.choice(secret_doors)
                    option.append(("SecretDoor", location, secret_door))
                valid_options.append(option)
            return valid_options
        # if encounter (creature to fight)
        if encounter:
            if not occupied:
                # need to resolve encounter
                option.append(("Encounter", location, last_exit))
                valid_options.append(option)
            return valid_options
        # there should always be at least one exit
        for exit in self.board.spaces[location].exits:
            exit_option = ("Move", location, exit)
            new_option = option + [exit_option]
            self.search_moves(player, exit.destination, exit, count-1, new_option, valid_options)
        return valid_options
        
    
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
    