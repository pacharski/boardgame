# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import a_game as ag
import board_game as bg


class GameView(bg.BoardView):
    def __init__(self, parent, board, image_path, size, **kwargs):
        super().__init__(parent, board, image_path, size, **kwargs)
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
        self.overlay_decks()
        self.overlay_hoards()
        self.overlay_hordes()
            
    def overlay_players(self):
        for player in self.players():
            self.overlay_player(player)

    def overlay_cards(self):
        for deck in self.deck():
            self.overlay_deck(deck)
        
    def overlay_creatures(self):
        for creature in self.horde():
            self.overlay_creature(creature)

    def overlay_treasures(self):
        for treasure in self.hoard():
            self.overlay_treasure(treasure)

    def overlay_player(self, player):
        print(player)
        
    def overlay_cards(self, card):
        print(card)
        
    def overlay_creatures(self, creature):
        print(creature)
        
    def overlay_treasures(self, treasure):
        print(treasure)
                                
    def on_key_press_ctrl_m(self, event):
        """Disable rotate_overlay"""
        pass
        
    def on_key_press(self, event):
        pass


# if __name__ == "__main__":
#     import os
#     import tkinter

#     here = os.path.abspath(__file__)
#     print()
#     print("Here", here)
#     json_path = os.path.join(os.path.dirname(here), "data/board.json" )
#     board = bg.Board.from_json_path(json_path)
 
#     root = tkinter.Tk()
#     root.title( "viewing" )
#     frame = tkinter.Frame( root )
#     frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
    
#     image_path = os.path.join(os.path.dirname(here), "data/board.png")
#     canvas = BoardView( frame, board, image_path, (400, 300),
#                          bg="white", highlightthickness=0 ) 
    
#     canvas.focus_set()    
#     tkinter.mainloop()

