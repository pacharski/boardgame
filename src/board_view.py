from enum import IntEnum
from resizable import ResizableImage
from model import Board, Point


class BoardView( ResizableImage ):
    cLevelColors = ["#11f", #0: Dark Blue
                    "#ff1", #1: Orange
                    "#3bf", #2: Light Blue
                    "#f11", #3: Dark Red
                    "#d17", #4: Magenta
                    "#d71", #5: Red
                    "#1f1", #6: Green
                   ]

    class Overlay( IntEnum ):
        cNone       = 0x00
        cCenters    = 0x01
        cSides      = 0x02
        cCorners    = 0x04
        cExits      = 0x08
        cIds        = 0x10
        cAll        = 0x1f

    def __init__(self, parent, board, image_path, size, **kwargs):
        width, height = size
        super().__init__(parent, image_path, width=width, height=height, **kwargs)
        self.board = board
        
        self.overlay = BoardView.Overlay.cNone
        
        self.bind("<Button-1>", self.on_mouse_left)
        self.bind("<B1-Motion>", self.on_mouse_move_left)
        self.bind("<Control-KeyPress-m>", self.on_key_press_ctrl_m)  
        self.bind("<Control-KeyPress-M>", self.on_key_press_ctrl_m)  
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out) 

    @property
    def overlay_off(self):
        return self.overlay == BoardView.Overlay.cNone

    @property
    def overlay_centers(self):
        return bool(self.overlay & BoardView.Overlay.cCenters)

    @property
    def overlay_sides(self):
        return bool(self.overlay & BoardView.Overlay.cSides)
    
    @property
    def overlay_corners(self):
        return bool(self.overlay & BoardView.Overlay.cCorners)
    
    @property
    def overlay_exits(self):
        return bool(self.overlay & BoardView.Overlay.cExits)
    
    @property
    def overlay_ids(self):
        return bool(self.overlay & BoardView.Overlay.cIds)
    
    @property
    def visible_bbox(self):
        return (0, 0, self.width, self.height)
        
    def set_overlay(self, mode):
        if mode == "ReadOnly":
            self.overlay = BoardView.Overlay.cNone
        elif mode == "EditSpaces":
            self.overlay = (BoardView.Overlay.cCenters 
                          | BoardView.Overlay.cIds
                          | BoardView.Overlay.cSides
                          | BoardView.Overlay.cCorners)
        elif mode == "EditExits":
            self.overlay = (BoardView.Overlay.cCenters
                          | BoardView.Overlay.cIds   
                          | BoardView.Overlay.cExits)
        self.master.master.title(mode)
        self.resize()
        
    def resize(self):
        super().resize()
        self.apply_overlay( self.view_port.bbox() )

    def apply_overlay(self, bbox):
        if not self.overlay_off:
            for id, space in self.board.spaces.items():
                self.overlay_space(space, bbox, self.visible_bbox)
            
    def overlay_center(self, id, point, radius, color, bbox, visible_bbox):
        self.overlay_point(point, radius, color, bbox, visible_bbox)

    def overlay_point(self, point, radius, color, bbox, visible_bbox):
        if self.circle_in_bbox(point, radius, bbox):
            x, y = self.view_port.map_to_visible(point.xy, visible_bbox)
            r_scaled = int((radius * self.view_port.scale) / 20)
            self.create_oval(x-r_scaled, y-r_scaled, x+r_scaled, y+r_scaled, 
                             outline="black", fill=color, width=1)

    def overlay_id(self, id, point, color, bbox, visible_bbox):
        self.overlay_text(point, str(id), color, bbox, visible_bbox)

    def circle_in_bbox(self, point, radius, bbox):
        left, upper, right, lower = bbox
        x, y = point.xy
        return ((x > (left - radius)) and (x < (right + radius))
            and (y > (upper - radius)) and (y < (lower + radius)))
        
    def point_in_bbox(self, point, bbox):
        left, upper, right, lower = bbox
        x, y = point.xy
        return (x >= left) and (x <= right) and (y >= upper) and (y <= lower)
                            
    def overlay_line(self, start, end, width, color, bbox, visible_bbox):
        if self.point_in_bbox(start, bbox) or self.point_in_bbox(end, bbox):
            x0, y0 = self.view_port.map_to_visible(start.xy, visible_bbox)
            x1, y1 = self.view_port.map_to_visible(end.xy, visible_bbox)
            self.create_line(x0, y0, x1, y1, fill=color, width=width)

    def overlay_text(self, center, text, color, bbox, visible_bbox):
        if self.point_in_bbox(center, bbox):
            x, y = self.view_port.map_to_visible(center.xy, visible_bbox)
            self.create_text((x, y), text=text, fill=color)

    def center_color(self, id, level):
        level_idx = level if level >= 0 and level < len(BoardView.cLevelColors) else 0
        return BoardView.cLevelColors[level_idx]
    
    def id_color(self, id, level):
        return "white" if level != 1 else "black"
                            
    def overlay_space(self, space, bbox, visible_bbox):
        if (space != None) and (space.center != None):
            level = space.level 
            level_color = BoardView.cLevelColors[max(0, level)]
            if self.overlay_centers:
                center_color = self.center_color(space.id, space.level)
                self.overlay_center(space.id, space.center, 5, center_color, bbox, visible_bbox)
            if self.overlay_ids:
                id_color = self.id_color(space.id, space.level)
                self.overlay_id(space.id, space.center, id_color, bbox, visible_bbox)
            if self.overlay_sides:
                # draw lines connecting vertices
                if len(space.vertices) > 1:
                    last_point = space.vertices[-1]
                    for point in space.vertices:
                        self.overlay_line(last_point, point, 1, "red", bbox, visible_bbox)
                        last_point = point
            if self.overlay_corners:
                # draw points for vertices
                for point in space.vertices:
                    self.overlay_point(point, 2, "red", bbox, visible_bbox)
                    last_point = point
            if self.overlay_exits:
                origin = space.center
                for exit in space.exits:
                    terminus = self.board.spaces[exit.destination].center
                    if self.overlay_centers or (terminus.xy > origin.xy):
                        self.overlay_line(origin, terminus, 2, "black", bbox, visible_bbox)

    def rotate_overlay(self):
        self.overlay = (self.overlay + 1) & BoardView.Overlay.cAll
        title = "Overlay:"
        title += (" Off"    if self.overlay_off     else "")
        title += (" Center" if self.overlay_centers else "")
        title += (" Id"     if self.overlay_ids     else "")
        title += (" Side"   if self.overlay_sides   else "")
        title += (" Corner" if self.overlay_corners else "")
        title += (" Exit"   if self.overlay_exits   else "")
        self.master.master.title( title )
        self.resize()
        
    def on_mouse_left( self, event ):
        self.focus_set()
        super().on_mouse_left( event )
        
    def on_mouse_move_left(self, event):
        if self.overlay_off:
            super().on_mouse_move_left( event )
    
    def on_focus_in(self, event):
        print("focus:in")

    def on_focus_out(self, event):
        print("focus:out")
        
    def on_key_press_ctrl_m(self, event):
        self.rotate_overlay()
        
    def on_key_press(self, event):
        pass


if __name__ == "__main__":
    import os
    import tkinter

    here = os.path.abspath(__file__)
    json_path = os.path.join(os.path.dirname(here), "../data/board.json" )
    board = Board.from_json_path(json_path)
 
    root = tkinter.Tk()
    root.title( "viewing" )
    frame = tkinter.Frame( root )
    frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
    
    # image_name = "dungeon/BoardView_cropped.png"
    image_path = os.path.join(os.path.dirname(here), "../data/board.png")
    canvas = BoardView( frame, board, image_path, (400, 300),
                         bg="white", highlightthickness=0 ) 
    
    canvas.focus_set()    
    tkinter.mainloop()

