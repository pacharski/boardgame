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

# Training
# def train_step(self, state, action, reward, next_state, done):
    
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
            action_choices.extend([[discard_action] + move + [space_action]
                                   for move in move_choices])
            challenge_choices = self.game.challenge_choices(self.player, card)
            action_choices.extend([[discard_action] + [challenge] 
                                   for challenge in challenge_choices])
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
    
    # def choose_player_to_challenge(self, card: ff.Card):
    #     players_to_challenge = self.game.challenge_choices(self.player)
    #     challenge_choices = []
    #     for player in players_to_challenge:
    #         challenge_choices.append([ff.GameAction("Challenge",
    #                                                 card=card,
    #                                                 location=player.location,
    #                                                 other_player=player)])
    #     return challenge_choices
                           
    # def challenge_player(self, card: ff.Card):
    #     """
    #         If win challenge, go to forward from challengee space
    #         If lose challenge, turn is over
    #     """
    #     challenge_choices = []
    #     players = [player for player in self.game.players 
    #                if ((player != self.player) and (player.location != None)
    #                and (player.location > self.player.location))]
    #     for player in players:
    #         challenge_choices.append([ff.GameAction("Challenge",
    #                                                 card=card,
    #                                                 location=player.location,
    #                                                 other_player=player)])
    #     return challenge_choices
       
    
if __name__ == "__main__":
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    