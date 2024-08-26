# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
import tkinter

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(here))

#from enum import IntEnum
import board_game as bg


class BoardViewer(bg.BoardView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        board = bg.Board.from_json_path(self.json_path)

        self.root = tkinter.Tk()
        self.root.title( "viewing" )
        frame = tkinter.Frame( self.root )
        frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
        super().__init__(frame, board, self.image_path, (400, 300),
                         bg="white", highlightthickness=0 ) 
        self.focus_set() 

    def bind_mouse(self):
        super().bind_mouse()

    def bind_keys(self):
        super().bind_keys()

    def bind_meta(self):
        super().bind_meta()  

    def apply_overlay(self, bbox):
        super().apply_overlay(bbox)
    
    def run(self):
        tkinter.mainloop()

    @property
    def json_path(self):
        return os.path.join(self.data_path, self.name + ".json")

    @property
    def image_path(self):
        return os.path.join(self.data_path, self.name + ".png")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "../data")
    bv = BoardViewer("board", data_path)
    bv.run()