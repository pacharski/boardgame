from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import random
import fafo as ff
import board_game as bg


class Agent(): 
    def __init__(self, player: ff.Player, game: ff.Game):
        self.player = player
        self.board = game.board
        self.game = game
        
    def turn(self):
        action_list = self.move()
        print("Turn", self.player.name, len(action_list))
        if action_list != None:
            for action in action_list:
                yield action
        
    def move(self):
        """ figure out the possible move options for the player, and pick one"""
        """
            draw pile - shuffle all monster cards and here cords (heros have value 8)
            heros allow matching here shortcut to be used (matches color, 1990 board has
             hero picture instead of star, these are the dupicate color shortcuts on the 
             82 board)

            draw card (should have 3 already)
            play card or challenge opponent
            play card:
                move spaces using value of card (1-7)
                Ending on red circle, ambush:
                    select card from hand
                    draw card
                    if select value (1-7) >= draw value:
                        move forward value of select
                    else
                        move backward value of draw
                    both cards are discarded
                Starting on, Passing over or onto a space with matching star color (shortcut)
                    Player can (may) take the shortcut if they played a card with the same color
                    This is all of players movement (end movement at destination end of shortcut)
            Challenge
                Select another player
                Both place card from hand face down
                If challenger card >= challenged
                    challenger moves to space in front of challenged
                else
                    end of turn
                cards are discarded, and players draw a new card to replace them
            Landing (end of turn) on space with another player
                combine cards from both hands, and select 3 to keep, return the rest to the other player

            Reach end to win
                Need exact count to end???
        """
        # Draw a card, and pick one of the four cards to either move, or challenge a player
        while len(self.player.hand) < 4:
            new_card = self.game.draw()
            self.player.hand.add(new_card)
            print(self.player.name, "draw", new_card, len(self.player.hand))

        valid_options = []
        for card in self.player.hand:
            valid_options.extend(self.move_ahead(card))
            #valid_options.extend(self.challenge_player(card))
        if len(valid_options) > 0:
            option = random.choice(valid_options)
            return option
        return []

    def move_ahead(self, card):
        """
            Move forward or shortcut
              Shortcut anytime on a shorcut space (begin, passing, end), can
               take shortcut and end movement
            Redefine connections/exits as Forward, Backward, Shortcut
            End movement on Empty, Ambush, Player, End
        """
        options = []  # move forward and moves with shortcuts
        if self.player.location == None:
            return options
        moves = []    # all of the move steps for this turn
        moves.append(("Discard", card))
        space: bg.Space = self.game.board.spaces[self.player.location]
        for _ in range(card.value):
            # if there are any shortcuts, create a new option with moves to this
            #  point and add the shortcut.  Save the shortcut options in options
            shortcuts = [exit for exit in space.exits if exit.barrier=="Shortcut"]
            if len(shortcuts) > 0:  # there should be only zero or one per space
                exit: bg.Exit = shortcuts[0]
                shortcut_option = [move for move in moves] # make a copy
                shortcut_option.append(("Shortcut", space.id, exit))
                options.append(shortcut_option)
            # record all forward move until the move count runs out in moves
            forwards = [exit for exit in space.exits if exit.barrier=="Forward"]
            if len(forwards) > 0: # there should be only one forward move per space
                exit: bg.Exit = forwards[0]
                moves.append(("Move", space.id, exit))
                space: bg.Space = self.game.board.spaces[exit.destination]
            forwards = [exit for exit in space.exits if exit.barrier=="Forward"]
            if len(forwards) == 0: 
                moves.append(("Finished", space.id))
                break
        options.append(moves)
        return options
    
    def challenge_player(self, card):
        """
            If win challenge, go to forward from challengee space
            If lose challenge, turn is over
        """
        challenges = []
        players = [player for player in self.game.players 
                   if ((player != self.player) and (player.location != None))]
        for player in players:
            challenges.append([("DrawCard", card), ("Challenge", player)])
        return challenges
    
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
        space = self.board.spaces[location]
        if (space.name != "") and (space.name != "Room"):
            # Big room has no limit on number of players landing there
            return False
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
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    