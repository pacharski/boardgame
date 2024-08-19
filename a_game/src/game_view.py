# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import a_game as ag
import board_game as bg


class GameView(bg.BoardView):
    def __init__(self, parent, game: ag.Game, image_path, size, **kwargs):
        super().__init__(parent, game.board, image_path, size, **kwargs)
        self.game = game
        self.bind_mouse()
        self.bind_keys()
        self.bind_meta()
        
    def bind_mouse(self):
        super().bind_mouse()
        
    def bind_keys(self):
        super().bind_keys()
        
    def bind_meta(self):
        super().bind_meta()
             
    def resize(self):
        super().resize()  # this also calls apply_overlay
        
    def apply_overlay(self, bbox):
        self.overlay_players()
        self.overlay_cards()
        self.overlay_treasures()
        self.overlay_creatures()
            
    def overlay_players(self):
        for player in self.game.players:
            self.overlay_player(player)

    def overlay_cards(self):
        for deck in self.game.decks:
            self.overlay_deck(deck)
        
    def overlay_creatures(self):
        for creature in self.game.horde:
            self.overlay_creature(creature)

    def overlay_treasures(self):
        for treasure in self.game.hoard:
            self.overlay_treasure(treasure)

    def overlay_player(self, player):
        print(player.marker)
        
    def overlay_deck(self, card):
        # print(card)
        pass
        
    def overlay_creature(self, creature):
        #print(creature)
        pass

    def overlay_treasure(self, treasure):
        #print(treasure)
        pass

    def on_key_press_ctrl_m(self, event):
        """Disable rotate_overlay"""
        pass
        
    def on_key_press(self, event):
        pass
