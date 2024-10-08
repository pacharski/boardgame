# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(here))

import tkinter
from enum import IntEnum
import board_game as bg


class FafoEditor( bg.BoardView ):
    class Mode( IntEnum ):
        cReadOnly      = 0
        cEditSpaces    = 1
        cEditExits     = 2
        cMax           = 3

    cLevelColors = ["#fff", #0: White        # Start, End, regular spaces
                    "#f00", #1: Red          # Circles
                    "#720", #2: Spider       # Brown
                    "#EE4", #3: Orc          # Yellow
                    "#060", #4: Kobold       # Dark Green
                    "#b22", #5: Goblin       # Red
                    "#f19", #6: Troll        # Pink
                    "#227", #7: Ogre         # Dark Blue
                    "#c61", #8: Werewolf     # Orange 
                    "#FA0", #9: Minotaur     # Orange-Yellow
                    "#ad3", #10: Mummy       # Light Green (yellow-green)
                    "#68f", #11: Giant       # Blue
                    "#000", #12: Vampire     # Black
                    "#f11", #13: Dragon      # Dark Red
                   ]

    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        board = bg.Board.from_json_path(self.json_path)
        
        self.root = tkinter.Tk()
        self.root.title( "cReadOnly" )
        frame = tkinter.Frame( self.root )
        frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
        super().__init__(frame, board, self.image_path, (400, 300),
                         bg="white", highlightthickness=0 ) 
        self.focus_set() 

        self.space = bg.Space()            # actively defining a new space
        self.connection = bg.Connection()  # actively defining a new connection
        self.text = ""                    # text entered while defining space or connection
        
        self.mode = FafoEditor.Mode.cReadOnly
        self.set_overlay("ReadOnly")
        
        # self.bind_mouse()
        # self.bind_keys()

    def bind_mouse(self):
        super().bind_keys()
        # Left click to mark points when in edit mode
        self.bind("<Button-1>", self.on_mouse_left)
        # Ignore mouse move events when in edit mode
        self.bind("<B1-Motion>", self.on_mouse_move_left)
        # double click to toggle edit mode
        # self.bind("<Double-ButtonPress-1>", self.on_mouse_double_left)  
        
    def bind_keys(self):    
        super().bind_keys()
        # esc to abort define space
        # enter to end define space
        # ctrl-z undo last mark
        # ctrl-s save marks to file
        # ctrl-m to change edit modes
        self.bind("<Control-KeyPress-z>", self.on_key_press_ctrl_z)  
        self.bind("<Control-KeyPress-Z>", self.on_key_press_ctrl_z)  
        self.bind("<Control-KeyPress-s>", self.on_key_press_ctrl_s)  
        self.bind("<Control-KeyPress-S>", self.on_key_press_ctrl_s)  
        # self.bind("<Control-KeyPress-m>", self.on_key_press_ctrl_m)  
        # self.bind("<Control-KeyPress-M>", self.on_key_press_ctrl_m)  
        self.bind("<KeyPress-Return>", self.on_key_press_return)  
        self.bind("<KeyPress-Escape>", self.on_key_press_escape)
        self.bind("<KeyPress>", self.on_key_press)
        
    def bind_meta(self):
        super().bind_meta()
    
    def run(self):
        tkinter.mainloop()

    @property
    def json_path(self):
        return os.path.join(self.data_path, self.name + ".json")

    @property
    def image_path(self):
        return os.path.join(self.data_path, self.name + ".jpg")
    
    @property
    def read_only(self):
        return self.mode == FafoEditor.Mode.cReadOnly

    @property
    def edit_spaces(self):
        return self.mode == FafoEditor.Mode.cEditSpaces
    
    @property
    def edit_exits(self):
        return self.mode == FafoEditor.Mode.cEditExits
 
    def resize(self):
        super().resize()

    def connection_valid(self):
        return self.connection.origin != None
    
    def space_id_in_connection(self, space_id):
        return (self.connection_valid()
            and ((space_id == self.connection.origin)
              or (space_id == self.connection.terminus)))
    
    def center_color(self, id, level):
        return ("black" if self.space_id_in_connection(id) else
                FafoEditor.cLevelColors[level]
               )
               
    def id_color(self, id, level):
        return ("white" if self.space_id_in_connection(id) else
                super().id_color(id, level)
               )
    
    def level_color(self, level):
        return FafoEditor.cLevelColors[max(0, level)]
                            
    def apply_overlay(self, bbox):
        super().apply_overlay(bbox)
        if self.edit_spaces:
            visible_bbox = (0, 0, self.width, self.height)
            self.overlay_space(self.space, bbox, visible_bbox)
    
    def find_point(self, point):
        return None, point
        
    def mark_space(self, point):
        print("MarkSpace", point)
        self.focus_set()
        xy = point.xy
        x, y = self.view_port.map_to_domain(xy, (0, 0, self.width, self.height))
        if self.space.center != None:
            #near, xy = self.find_point( xy )
            self.space.add_vertex(bg.Point(x=x, y=y))
        else:
            # print("SetCenter", xy)
            self.space.center = bg.Point(x=x, y=y)
        self.resize()
        
    def unmark_space(self):
        self.space.remove_last_vertex()

    def mark_connection(self, point):
        self.focus_set()
        x, y = self.view_port.map_to_domain(point.xy, (0, 0, self.width, self.height))
        id, _ = self.board.find_space(bg.Point(x, y))
        if (self.connection.origin == None) or (id == self.connection.origin):
            self.connection.origin = id
        else:
            self.connection.terminus = id
        # redraw to show connection in progress
        self.resize()
        
    def unmark_connection(self):
        if self.connection.origin != None:
            if self.connection.terminus != None:
                self.connection.terminus = None
            else:
                self.connection.origin = None
        
    def rotate_mode(self):
        if self.mode == FafoEditor.Mode.cReadOnly:
            self.mode = FafoEditor.Mode.cEditSpaces
            self.set_overlay("EditSpaces")
        elif self.mode == FafoEditor.Mode.cEditSpaces:
            self.mode = FafoEditor.Mode.cEditExits
            self.set_overlay("EditExits")
        else:
            self.mode = FafoEditor.Mode.cReadOnly
            self.set_overlay("ReadOnly")
        self.abandon_space()
        self.abandon_connection()
        
    def save_space(self, text=""):
        print("SaveSpace", self.space.center, text)
        if self.space.center != None:
            parts = text.split(',')
            level = int(parts[0]) if (len(parts) > 0) and (len(parts[0]) > 0) else 0
            name  = parts[1] if len(parts) > 1 else ""
            self.board.add_space(
                bg.Space(name=name, level=level, center=self.space.center,
                         vertices=[bg.Point(x=v.x, y=v.y) for v in self.space.vertices],
                         exits=[])
            )
            self.space.reset()
            self.resize()
        
    def abandon_space(self):
        self.space.reset()
        self.resize()

    def decode_barrier(self, text, idx):
        idx = max(-1, min(idx, len(text)-1))
        barrier = text[idx] if idx >= 0 else ""
        return ("" if barrier == "" else
                "Secret Door" if barrier in "sS" else
                "Door" if barrier in "dD" else
                "")
            
    def save_connection(self, text=""):
        if ((self.connection.origin != None) 
        and (self.connection.terminus != None)):
            forward = self.decode_barrier(text, 0)
            backward = self.decode_barrier(text, 1)
            self.board.spaces[self.connection.origin].add_exit(
                bg.Exit(destination=self.connection.terminus, barrier=forward)
            )
            self.board.spaces[self.connection.terminus].add_exit(
                bg.Exit(destination=self.connection.origin, barrier=backward)
            )
        self.connection.reset()
        self.resize()

    def abandon_connection(self):
        self.connection.reset()
        self.resize()

    def save_to_file(self):
        print("SaveToFile")
        self.board.save_to_json_path(json_path=self.json_path)
    
    def on_mouse_left( self, event ):
        self.focus_set()
        if self.edit_spaces:  
            self.zooming = False
            self.mark_space(bg.Point(x=event.x, y=event.y))
        elif self.edit_exits: 
            self.zooming = False
            self.mark_connection(bg.Point(x=event.x, y=event.y))
        else:
            super().on_mouse_left( event )
        
    def on_mouse_move_left(self, event):
        if not self.viewing():
           pass
        else:
            super().on_mouse_move_left( event )
    
    def on_mouse_double_left( self, event ):
        self.abandon_space()
        self.abandon_connection()
        self.focus_set()
        self.rotate_mode()
        
    def on_key_press_return(self, event):
        if self.edit_spaces:
            self.save_space(self.text)
            self.space.reset()
            self.text = ""
        elif self.edit_exits:
            self.save_connection(self.text)
            self.connection.reset()
            self.text = ""

    def on_key_press_escape(self, event):
        if self.edit_spaces:
            self.abandon_space()
        elif self.edit_exits:
            self.abandon_connection()
        self.text = ""

    def on_focus_in(self, event):
        self.abandon_space()
        self.abandon_connection()
        print("focus:in")

    def on_focus_out(self, event):
        print("focus:out")
        self.abandon_space()
        self.abandon_connection()

    def on_key_press_ctrl_z(self, event):
        self.unmark_space()
        self.unmark_connection()

    def on_key_press_ctrl_s(self, event):
        self.save_to_file()

    def on_key_press_ctrl_m(self, event):
        self.abandon_space()
        self.abandon_connection()
        self.rotate_mode()
        
    def on_key_press(self, event):
        # print("KeyPress", event, self.space,
        #        self.space.center() if self.space != None else "None",
        #        self.space.level() if self.space != None else "None"
        # )
        self.text += event.char



if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "../fafo/data")
    bv = FafoEditor("fafo", data_path)
    bv.run()
