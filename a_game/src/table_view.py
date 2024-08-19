# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import tkinter

import a_game as ag
import board_game as bg


class TableView(tkinter.Frame):
    def __init__(self, parent, game, image_path, size, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_view(parent, game, image_path, size)
        # self.bind_mouse()
        # self.bind_keys()
        # self.bind_meta()
        
    # def bind_mouse(self):
    #     super().bind_mouse()
        
    # def bind_keys(self):
    #     super().bind_keys()
        
    # def bind_meta(self):
    #     super().bind_meta()

    def create_view(self, root, board, image_path, size):
        root.title("TableView")
        width, height = size
        root.geometry("{}x{}+0+0".format(width, height))
        # root should be configured as 'resizable' grid with 'weight'
        tkinter.Grid.rowconfigure(root, 0, weight=1)
        tkinter.Grid.columnconfigure(root, 0, weight=1)
        self.grid(row=0, column=0, sticky="news")

        side_width, side_height = int(width / 8), int(height / 8)
        center_width, center_height = int((width * 3) / 4), int((height * 3) / 4)
        self.center = bg.ResizableImage(self, image_path, 
                                        width=center_width, height=center_height,
                                        bg="white", highlightthickness=0)
        self.center.grid(column=1, row=1, columnspan=2, rowspan=2, sticky="news")
        
        self.corner00 = tkinter.Canvas(self, width=side_width, height=side_height,
                                       bg="grey", highlightthickness=0)
        self.corner00.grid(column=0, row=0)
        self.corner30 = tkinter.Canvas(self, width=side_width, height=side_height,
                                       bg="grey", highlightthickness=0)
        self.corner30.grid(column=3, row=0)
        self.corner03 = tkinter.Canvas(self, width=side_width, height=side_height, 
                                       bg="grey", highlightthickness=0)
        self.corner03.grid(column=0, row=3)
        self.corner33 = tkinter.Canvas(self, width=side_width, height=side_height, 
                                       bg="grey", highlightthickness=0)
        self.corner33.grid(column=3, row=3)
        
        self.side_n = tkinter.Canvas(self, width=center_width, height=side_height,  
                                     bg="green", highlightthickness=0)
        self.side_n.grid(column=1, row=0, columnspan=2, sticky="ew")
        self.side_e = tkinter.Canvas(self, width=side_width, height=center_height, 
                                     bg="green", highlightthickness=0)
        self.side_e.grid(column=3, row=1, rowspan=2, sticky="ns")
        self.side_w = tkinter.Canvas(self, width=side_width, height=center_height, 
                                     bg="green", highlightthickness=0)
        self.side_w.grid(column=0, row=1, rowspan=2, sticky="ns")
        self.side_s = tkinter.Canvas(self, width=center_width, height=side_height,  
                                     bg="green", highlightthickness=0)
        self.side_s.grid(column=1, row=3, columnspan=2, sticky="ew")

        tkinter.Grid.columnconfigure(self, tuple(range(4)), weight=side_width)
        tkinter.Grid.rowconfigure(self, tuple(range(4)), weight=side_height)
        tkinter.Grid.columnconfigure(self, tuple(range(1,2)), weight=center_width)
        tkinter.Grid.rowconfigure(self, tuple(range(1,2)), weight=center_height)

             
    def resize(self):
        super().resize()  # this also calls apply_overlay
        
    def apply_overlay(self, bbox):
        self.overlay_players()
        self.overlay_cards()
        self.overlay_treasures()
        self.overlay_creatures()
            
    def overlay_players(self):
        for player in self.players():
            self.overlay_player(player)

    def overlay_cards(self):
        for deck in self.deck():
            self.overlay_card(deck)
        
    def overlay_creatures(self):
        for creature in self.horde():
            self.overlay_creature(creature)

    def overlay_treasures(self):
        for treasure in self.hoard():
            self.overlay_treasure(treasure)

    def overlay_player(self, player):
        print(player)
        
    def overlay_card(self, card):
        print(card)
        
    def overlay_creature(self, creature):
        print(creature)
        
    def overlay_treasure(self, treasure):
        print(treasure)
                                
    def on_key_press_ctrl_m(self, event):
        """Disable rotate_overlay"""
        pass
        
    def on_key_press(self, event):
        pass