import os
import sys
import tkinter
from enum import IntEnum

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import Board, Point, Space, Path, Exit
from board_view import BoardView


if __name__ == "__main__":
    here = os.path.abspath(__file__)
    image_path = os.path.join(os.path.dirname(here), "../data/board.png")
    json_path = os.path.join(os.path.dirname(here), "../data/board.json" )
 
    root = tkinter.Tk()
    root.title( "cReadOnly" )
    frame = tkinter.Frame( root )
    frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
    
    canvas = BoardEdit( frame, json_path, image_path, (400, 300),
                        bg="white", highlightthickness=0 ) 
        
    canvas.focus_set()    
    tkinter.mainloop()

