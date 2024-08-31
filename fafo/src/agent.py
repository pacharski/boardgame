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
        
    def turn(self, card=None):
        action_list = self.move(card)
        if action_list != None:
            for action in action_list:
                yield action
        
    def draw_cards(self, use_card):
        # Replenish hand to 3, plus a new card for the turn
        hand_cards = 3 if use_card != None else 4
        while len(self.player.hand) < hand_cards:
            new_card = self.game.draw(name=self.player.name)
            self.player.hand.add(new_card)
            # print(self.player.name, "draw", new_card, len(self.player.hand))

    def move(self, use_card=None):
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
        self.draw_cards(use_card)
        # figure out all of the possible move/challenge options for this turn
        space: bg.Space = self.game.board.spaces[self.player.location]
        valid_options = []
        card_options = self.player.hand if use_card == None else [use_card]
        for card in card_options:
            self.move_ahead(card.value, card, space, None, valid_options, 
                            ambushed=(use_card != None))
            if not use_card:
                self.challenge_player(card, valid_options)
        option = (random.choice(valid_options) if len(valid_options) > 0 else [])
        return option
        
    def move_ahead(self, count, card, space, in_moves=None, options=None,
                   ambushed=False):
        #print("MoveAhead", ambushed, space.id, space.name, len(in_moves) if in_moves != None else None)
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
        moves = (in_moves[:] if in_moves != None else 
                 [("Discard", card)] if not ambushed else
                 [])
        if count == 0:
            options.append(moves)  # add a copy of moves to the list of options
            return 
        
        use_exits = ["Shortcut", "Forward"] if not ambushed else ["Forward"]
        exits = [exit for exit in space.exits
                 if (exit.barrier in use_exits)]
        if len(exits) == 0: 
            print(self.player.name, "Finished in space NoExits", space.id, space.name)
            moves.append(("Finished", space.id))
            options.append(moves)
            return
        
        for exit in exits:
            moves_copy = moves[:]
            if exit.barrier == "Shortcut":
                # check if shortcut can be taken (card level, hero)
                if card.name in [name.strip() for name in space.name.split(',')]:
                    moves_copy.append(("Shortcut", space.id, exit))
                    self.move_ahead(0, card, 
                                    self.game.board.spaces[exit.destination],
                                    moves_copy, options, ambushed)
            else:
                moves_copy.append(("Move", space.id, exit))
                self.move_ahead(count-1, card, 
                                self.game.board.spaces[exit.destination],
                                moves_copy, options, ambushed)
                
    def challenge_player(self, card: ff.Card, options):
        """
            If win challenge, go to forward from challengee space
            If lose challenge, turn is over
        """
        players = [player for player in self.game.players 
                   if ((player != self.player) and (player.location != None))]
        for player in players:
            options.append([("DrawCard", card), 
                            ("Discard", card),
                            ("Challenge", card, player)
                          ])
        return 
       
    
if __name__ == "__main__":
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    