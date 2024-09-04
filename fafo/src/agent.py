from pathlib import Path
# print('Running' if __name__ == '__main__' else
#       'Importing', Path(__file__).resolve())

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
        # print(self.player.name, len(self.player.hand))
        for card in self.player.hand:
            shortcut_keys = [card.name] if card != None else []
            discard_action = ff.GameAction("Discard", card=card)
            space_action = ff.GameAction("SpaceAction")
            move_choices = self.game.move_choices(space, card.value, 
                                                  shortcut_keys, exit_types)
            action_choices.extend([[discard_action] + m + [space_action]
                                   for m in move_choices])
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
        action_choices.extend(self.game.move_choices(space, card.value, exit_types, 
                                                     final=True))
        return random.choice(action_choices) if (len(action_choices) > 0) else []
        
    def choose_action_after_ambush_loss(self, card):
        """ enumerate all possible moves after ambush win
            card supplied, should have 3 cards in hand
        """
        space = self.game.space_at_location(self.player.location)
        exit_types = ("Backward")
        action_choices = []
        action_choices.extend(self.game.move_choices(space, card.value, exit_types,
                                                     final=True))
        return random.choice(action_choices) if (len(action_choices) > 0) else []
    
    def choose_card_for_ambush(self):
        """select and remove a card from player hand to use for ambush"""
        return self.player.hand.draw()
    
    def choose_player_to_share_cards(self, other_players: list):
        others = sorted(other_players, key=lambda p:p.location, reverse=True)
        return others[0] if len(others) > 0 else None
        # player = random.choice(other_players) if len(other_players) > 0 else None
        # return player                        

    def choose_shared_cards_to_keep(self, all_cards: list, other_player: ff.Player):
        #random.shuffle(all_cards)
        all_cards.sort(key=lambda card:card.value, reverse=True)
        return all_cards[:3], all_cards[3:]
        
    def move_choices(self, space: bg.Space, moves_left: int, card: ff.Card,
                           exit_types=("Forward", "Shortcut"), final=False):
        """ Return a list of possible move action lists starting at space and
             using the number of moves list by taking available exit_types
        """ 
        if moves_left == 0:
            moves = [[ff.GameAction(self.player, card, 
                                   ("Final" if final else "SpaceAction"))]]
        else: 
            moves = [] 
            exits = [e for e in space.exits if ((e.barrier in exit_types)
                                            and self.game.exit_available(e, space, card))]
            for exit in exits:
                exit_action = ff.GameAction(self.player, card, "Move",
                                            location=exit.destination,
                                            other_player=None)
                next_choices = self.move_choices(self.game.space_at_location(exit.destination),
                                                 moves_left-1, card, exit_types, final)
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
        challenge_choices = []
        players = [player for player in self.game.players 
                   if ((player != self.player) and (player.location != None)
                   and (player.location > self.player.location))]
        for player in players:
            challenge_choices.append([ff.GameAction("Challenge",
                                                    card=card,
                                                    location=player.location,
                                                    other_player=player)])
        return challenge_choices
       
    
if __name__ == "__main__":
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    