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
        new_card = self.game.draw()
        self.player.hand.add(new_card)

        valid_options = []
        for card in self.player.hand:
            valid_options.extend(self.move_ahead(card))
            valid_options.extend(self.challenge_player(card))

    def move_ahead(self, card):
        return []
    
    def challenge_player(self, card):
        return []
    
    
if __name__ == "__main__":
    game = ff.Game("fafo", os.path.join(os.path.dirname(here), "data"))
    agents = [ff.Agent(player, game) for player in game.players]
    print(game)
    
    if len(agents) > 0:
        actions = agents[0].move()
        print("Action", actions)
    