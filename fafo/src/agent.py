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
        
    def draw_cards(self):
        # Replenish hand to 3, plus a new card for the turn
        while len(self.player.hand) < 4:
            new_card = self.game.draw()
            self.player.hand.add(new_card)
            print(self.player.name, "draw", new_card, len(self.player.hand))

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
        if self.player.location == None:
            return []
        self.draw_cards()
        # figure out all of the possible move/challenge options for this turn
        space: bg.Space = self.game.board.spaces[self.player.location]
        valid_options = []
        for card in self.player.hand:
            self.move_ahead(card.value, card, space, None, valid_options)
            self.challenge_player(card, valid_options)
        option = (random.choice(valid_options) if len(valid_options) > 0 else [])
        return option
        
    def move_ahead(self, count, card, space, moves=None, options=None):
        """
        Move forward or shortcut
            Shortcut anytime on a shorcut space (begin, passing, end), can
            take shortcut and end movement
        Redefine connections/exits as Forward, Backward, Shortcut
        End movement on Empty, Ambush, Player, End
        """
        options = options if options != None else []
        if self.player.location == None:
            return options
        moves = moves if moves != None else [("Discard", card)]

        if count == 0:
            options.append(moves[:])  # add a copy of moves to the list of options
            return 
        
        exits = [exit for exit in space.exits
                 if (exit.barrier in ("Shortcut", "Forward"))]
        if len(exits) == 0: 
            moves.append(("Finished", space.id))
            options.append(moves[:])
            return
        
        for exit in exits:
            moves_copy = moves[:]
            if exit.barrier == "Shortcut":
                # check if shortcut can be taken (card level, hero)
                moves_copy.append(("Shortcut", space.id, exit))
                space: bg.Space = self.game.board.spaces[exit.destination]
                self.move_ahead(0, card, space, moves_copy, options)
            else:
                moves_copy.append(("Move", space.id, exit))
                space: bg.Space = self.game.board.spaces[exit.destination]
                self.move_ahead(count-1, card, space, moves_copy, options)
    
    def challenge_player(self, card: ff.Card, options):
        """
            If win challenge, go to forward from challengee space
            If lose challenge, turn is over
        """
        players = [player for player in self.game.players 
                   if ((player != self.player) and (player.location != None))]
        for player in players:
            options.append([("DrawCard", card), 
                            ("Challenge", card, player)])
        return 
    
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
    