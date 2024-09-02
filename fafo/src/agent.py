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
        
    def choose_action(self):
        """ Return one turn action: 
              Draw a card, Play a card, move or challenge using that card
        """
        # Enumerate all possible card draws and actions, then pick one
        self.player.hand.add(self.game.draw()) # should have 4 cards now
        space = self.game.space_at_location(self.player.location)
        exit_types = ("Forward", "Shortcut")
        action_choices = []
        for card in self.player.hand:
            discard_action = ff.GameAction(self.player, card, "Discard")
            move_choices = self.move_choices(space, card.value, card, exit_types)
            action_choices.extend([[discard_action] + m for m in move_choices])
            challenge_choices = self.challenge_player(card)
            action_choices.extend([[discard_action] + c for c in challenge_choices])
        return random.choice(action_choices) if (len(action_choices) > 0) else []
        
    def choose_action_after_ambush_win(self, card):
        """ Return a set of moves using Forward exits only (no shortcuts)
            Card is supplied (should have 3 cards in hand)
        """
        space = self.game.space_at_location(self.player.location)
        exit_types = ("Forward")
        action_choices = []
        action_choices.extend(self.move_choices(space, card.value, card, exit_types))
        return random.choice(action_choices) if (len(action_choices) > 0) else []
        
    def choose_action_after_ambush_loss(self, card):
        """ enumerate all possible moves after ambush win
            card supplied, should have 3 cards in hand
        """
        space = self.game.space_at_location(self.player.location)
        exit_types = ("Backward")
        action_choices = []
        action_choices.extend(self.move_choices(space, card.value, card, exit_types))
        return random.choice(action_choices) if (len(action_choices) > 0) else []
        
    def move_choices(self, space: bg.Space, moves_left: int, card: ff.Card,
                           exit_types=("Forward", "Shortcut")):
        """ Return a list of possible move action lists starting at space and
             using the number of moves list by taking available exit_types
        """ 
        moves = []
        if moves_left > 0:  
            exits = [e for e in space.exits if ((e.barrier in exit_types)
                                            and self.game.exit_available(e, space, card))]
            for exit in exits:
                exit_action = ff.GameAction(self.player, card, "Move",
                                            location=exit.destination,
                                            other_player=None)
                next_choices = self.move_choices(self.game.space_at_location(exit.destination),
                                                 moves_left-1, card, exit_types)
                 # at the end, next_choices will be an empty list
                if len(next_choices) > 0:
                    for move_choice in next_choices:
                        extended = [exit_action]
                        extended.extend(move_choice)
                        moves.append(extended)
                else:
                    moves.append([exit_action])
        return moves
                        
    def challenge_player(self, card: ff.Card):
        """
            If win challenge, go to forward from challengee space
            If lose challenge, turn is over
        """
        challenges = []
        players = [player for player in self.game.players 
                   if ((player != self.player) and (player.location != None))]
        for player in players:
            challenges.append([ff.GameAction(self.player, card, "Challenge",
                                             location=player.location,
                                             other_player=player)])
        return challenges
       
    
if __name__ == "__main__":
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    