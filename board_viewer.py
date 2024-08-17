# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
#import sys
from enum import IntEnum

import board_game as bg
import tkinter



class BoardViewer(bg.BoardView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.board_json_path = os.path.join(data_path, name + ".json")
        board = bg.Board.from_json_path(self.json_path)

        self.root = tkinter.Tk()
        self.root.title( "viewing" )
        frame = tkinter.Frame( self.root )
        frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
        self.canvas = bg.BoardView(frame, board, self.image_path, (400, 300),
                                   bg="white", highlightthickness=0 ) 
        self.canvas.focus_set()    
    
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
    data_path = os.path.join(here, "data")
    bv = BoardViewer("board", data_path)
    bv.run()