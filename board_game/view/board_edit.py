from enum import IntEnum

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from view.board_view import BoardView
from model.board import Board
from model.point import Point
from model.space import Space
from model.path import Path
from model.exit import Exit


class BoardEdit( BoardView ):
    class Mode( IntEnum ):
        cReadOnly      = 0
        cEditSpaces    = 1
        cEditExits     = 2
        cMax           = 3

    def __init__(self, parent, json_path, image_path, size, **kwargs):
        self.json_path = json_path
        self.board = Board.from_json_path(self.json_path)
        super().__init__(parent, self.board, image_path, size, **kwargs)
        
        self.space = Space()
        self.path = Path()
        self.text = ""
        
        self.mode = BoardEdit.Mode.cReadOnly
        self.set_overlay("ReadOnly")
        
        # Left click to mark points when in edit mode
        self.bind("<Button-1>", self.on_mouse_left)
        # Ignore mouse move events when in edit mode
        self.bind("<B1-Motion>", self.on_mouse_move_left)
        # double click to toggle edit mode
        # self.bind("<Double-ButtonPress-1>", self.on_mouse_double_left)  
        # esc to abort define space
        # enter to end define space
        # ctrl-z undo last mark
        # ctrl-s save marks to file
        # ctrl-m to change edit modes
        self.bind("<Control-KeyPress-z>", self.on_key_press_ctrl_z)  
        self.bind("<Control-KeyPress-Z>", self.on_key_press_ctrl_z)  
        self.bind("<Control-KeyPress-s>", self.on_key_press_ctrl_s)  
        self.bind("<Control-KeyPress-S>", self.on_key_press_ctrl_s)  
        self.bind("<Control-KeyPress-m>", self.on_key_press_ctrl_m)  
        self.bind("<Control-KeyPress-M>", self.on_key_press_ctrl_m)  
        self.bind("<KeyPress-Return>", self.on_key_press_return)  
        self.bind("<KeyPress-Escape>", self.on_key_press_escape)
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out) 

    @property
    def read_only(self):
        return self.mode == BoardEdit.Mode.cReadOnly

    @property
    def edit_spaces(self):
        return self.mode == BoardEdit.Mode.cEditSpaces
    
    @property
    def edit_exits(self):
        return self.mode == BoardEdit.Mode.cEditExits
 
    def resize(self):
        super().resize()

    def path_valid(self):
        return self.path.origin != None
    
    def space_id_in_path(self, space_id):
        return (self.path_valid()
            and ((space_id == self.path.origin)
              or (space_id == self.path.terminus)))
    
    def center_color(self, id, level):
        return ("black" if self.space_id_in_path(id) else
                super().center_color(id, level) 
               )
               
    def id_color(self, id, level):
        return ("white" if self.space_id_in_path(id) else
                super().id_color(id, level)
               )
                            
    def apply_overlay(self, bbox):
        super().apply_overlay(bbox)
        if self.edit_spaces:
            visible_bbox = (0, 0, self.width, self.height)
            self.overlay_space(self.space, bbox, visible_bbox)
    
    # def overlay_point(self, point, radius, color, bbox, visible_bbox):
    #     if self.point_in_
    #     if self.circle_in_bbox(point, radius, bbox):
    #         x, y = self.view_port.map_to_visible(point.xy, visible_bbox)
    #         r_scaled = int((radius * self.view_port.scale) / 20)
    #         self.create_oval(x-r_scaled, y-r_scaled, x+r_scaled, y+r_scaled, 
    #                          outline="black", fill=color, width=1)
            
    # def overlay_new_space(self, bbox, visible_bbox):
    #     left, upper, right, lower = bbox
    #     if self.space != None:
    #         r = 5
    #         rs = int((r * self.view_port.scale) / 20)
    #         if self.space.center != None:
    #             x, y = self.space.center.xy
    #             if  (x > (left - r) and x < (right + r)
    #              and y > (upper - r) and y < (lower + r)):
    #                 x, y = self.view_port.map_to_visible((x, y), visible_bbox)
    #                 self.create_oval( x-rs, y-rs, x+rs, y+rs, outline="#11f",
    #                                   fill="#11f", width=0)
    #         r = 2
    #         rs = int((r * self.view_port.scale) / 20)
    #         for point in self.space.vertices:
    #             x, y = point.xy
    #             if  (x > (left - r) and x < (right + r)
    #              and y > (upper - r) and y < (lower + r)):
    #                 # map xy from domain to canvas, then draw
    #                 x, y = self.view_port.map_to_visible((x, y), visible_bbox)
    #                 self.create_oval( x-rs, y-rs, x+rs, y+rs, outline="#f11",
    #                                   fill="#f11", width=0)

    def find_point(self, point):
        return None, point
        
    def mark_space(self, point):
        self.focus_set()
        xy = point.xy
        x, y = self.view_port.map_to_domain(xy, (0, 0, self.width, self.height))
        if self.space.center != None:
            #near, xy = self.find_point( xy )
            self.space.add_vertex(Point(x=x, y=y))
        else:
            # print("SetCenter", xy)
            self.space.center = Point(x=x, y=y)
        self.resize()
        
    def unmark_space(self):
        self.space.remove_last_vertex()

    def mark_path(self, point):
        self.focus_set()
        x, y = self.view_port.map_to_domain(point.xy, (0, 0, self.width, self.height))
        id, _ = self.board.find_space(Point(x, y))
        if (self.path.origin == None) or (id == self.path.origin):
            self.path.origin = id
        else:
            self.path.terminus = id
        # redraw to show path in progress
        self.resize()
        
    def unmark_path(self):
        if self.path.origin != None:
            if self.path.terminus != None:
                self.path.terminus = None
            else:
                self.path.origin = None
        
    def rotate_mode(self):
        if self.mode == BoardEdit.Mode.cReadOnly:
            self.mode = BoardEdit.Mode.cEditSpaces
            self.set_overlay("EditSpaces")
        elif self.mode == BoardEdit.Mode.cEditSpaces:
            self.mode = BoardEdit.Mode.cEditExits
            self.set_overlay("EditExits")
        else:
            self.mode = BoardEdit.Mode.cReadOnly
            self.set_overlay("ReadOnly")
        self.abandon_space()
        self.abandon_path()
        
    def save_space(self, text=""):
        if self.space.center != None:
            parts = text.split(',')
            level = int(parts[0]) if (len(parts) > 0) and (len(parts[0]) > 0) else 0
            name  = parts[1] if len(parts) > 1 else ""
            self.board.add_space(
                Space(name=name, level=level, center=self.space.center,
                      vertices=[Point(x=v.x, y=v.y) for v in self.space.vertices],
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
            
    def save_path(self, text=""):
        if ((self.path.origin != None) 
        and (self.path.terminus != None)):
            forward = self.decode_barrier(text, 0)
            backward = self.decode_barrier(text, 1)
            self.board.spaces[self.path.origin].add_exit(
                Exit(destination=self.path.terminus, barrier=forward)
            )
            self.board.spaces[self.path.terminus].add_exit(
                Exit(destination=self.path.origin, barrier=backward)
            )
        self.path.reset()
        self.resize()

    def abandon_path(self):
        self.path.reset()
        self.resize()

    def save_to_file(self):
        print("SaveToFile")
        self.board.save_to_json_file(json_path=self.json_path)
    
    def on_mouse_left( self, event ):
        self.focus_set()
        if self.edit_spaces:  
            self.zooming = False
            self.mark_space(Point(x=event.x, y=event.y))
        elif self.edit_exits: 
            self.zooming = False
            self.mark_path(Point(x=event.x, y=event.y))
        else:
            super().on_mouse_left( event )
        
    def on_mouse_move_left(self, event):
        if not self.viewing():
           pass
        else:
            super().on_mouse_move_left( event )
    
    def on_mouse_double_left( self, event ):
        self.abandon_space()
        self.abandon_path()
        self.focus_set()
        self.rotate_mode()
        
    def on_key_press_return(self, event):
        if self.edit_spaces:
            self.save_space(self.text)
            self.space.reset()
            self.text = ""
        elif self.edit_exits:
            self.save_path(self.text)
            self.path.reset()
            self.text = ""

    def on_key_press_escape(self, event):
        if self.edit_spaces:
            self.abandon_space()
        elif self.edit_exits:
            self.abandon_path()
        self.text = ""

    def on_focus_in(self, event):
        self.abandon_space()
        self.abandon_path()
        print("focus:in")

    def on_focus_out(self, event):
        print("focus:out")
        self.abandon_space()
        self.abandon_path()

    def on_key_press_ctrl_z(self, event):
        self.unmark_space()
        self.unmark_path()

    def on_key_press_ctrl_s(self, event):
        self.save_to_file()

    def on_key_press_ctrl_m(self, event):
        self.abandon_space()
        self.abandon_path()
        self.rotate_mode()
        
    def on_key_press(self, event):
        # print("KeyPress", event, self.space,
        #        self.space.center() if self.space != None else "None",
        #        self.space.level() if self.space != None else "None"
        # )
        self.text += event.char



if __name__ == "__main__":
    import os
    import tkinter
    
    here = os.path.abspath(__file__)
    image_path = os.path.join(os.path.dirname(here), "../../data/board.png")
    json_path = os.path.join(os.path.dirname(here), "../../data/board.json" )
 
    root = tkinter.Tk()
    root.title( "cReadOnly" )
    frame = tkinter.Frame( root )
    frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
    
    canvas = BoardEdit( frame, json_path, image_path, (400, 300),
                        bg="white", highlightthickness=0 ) 
        
    canvas.focus_set()    
    tkinter.mainloop()

