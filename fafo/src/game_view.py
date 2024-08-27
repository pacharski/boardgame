# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import fafo as ff
import board_game as bg


class GameView(bg.BoardView):
    def __init__(self, parent, game: ff.Game, image_path, size, **kwargs):
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
        
    def overlay_players(self):
        for player in self.game.players:
            self.overlay_player(player)

    def overlay_cards(self):
        for deck in self.game.draw_pile:
            self.overlay_deck(deck)
        
    def overlay_player(self, player):
        scale = self.view_port.scale / 20
        if player.location != None:
            #find center point for location
            space = self.board.find_space_by_location(player.location)
            xy = self.view_port.map_to_visible(space.center.xy, self.visible_bbox)
            bg.MarkerView(player.marker).draw(self, xy, scale)
        
    def overlay_deck(self, card):
        # print(card)
        pass
        
    def on_key_press_ctrl_m(self, event):
        """Disable rotate_overlay"""
        pass
        
    def on_key_press(self, event):
        pass
