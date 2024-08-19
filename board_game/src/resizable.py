
from PIL import Image, ImageTk
import tkinter


class ViewPort():
    def __init__(self, domain):
        self.domain = domain # width,height of thing being viewed
        self.scale = 10 # 10=1x, 20=2x, etc.  5=1/2x
        self.focus = ( int( self.domain[0] / 2 ), int( self.domain[1] / 2 ) )

    def width( self ):
        return int( ( self.domain[0] * 10 ) / self.scale ) if self.scale > 0 else 0
 
    def height( self ):
        return int( ( self.domain[1] * 10 ) / self.scale ) if self.scale > 0 else 0

    def map_to_domain( self, xy, bbox ):
        bb_left, bb_upper, bb_right, bb_lower = bbox
        bb_width, bb_height = ( bb_right - bb_left ), ( bb_lower - bb_upper )
        do_left, do_upper, do_right, do_lower = self.bbox()
        do_width, do_height = ( do_right - do_left ), ( do_lower - do_upper )
        x, y = xy
        x = int( ( x - bb_left  ) * do_width  / bb_width  ) + do_left
        y = int( ( y - bb_upper ) * do_height / bb_height ) + do_upper
        return ( x, y )  

    def map_to_visible( self, xy, bbox ):
        bb_left, bb_upper, bb_right, bb_lower = bbox
        bb_width, bb_height = ( bb_right - bb_left ), ( bb_lower - bb_upper )
        do_left, do_upper, do_right, do_lower = self.bbox()
        do_width, do_height = ( do_right - do_left ), ( do_lower - do_upper )
        x, y = xy
        x = int( ( x - do_left  ) * bb_width  / do_width  ) + bb_left
        y = int( ( y - do_upper ) * bb_height / do_height ) + bb_upper
        return ( x, y )  

    def bbox( self ):
        left, upper = self.left_upper()
        width, height = self.width(), self.height()
        right = left + width - 1 if width > 0 else left
        lower = upper + height - 1 if height > 0 else upper
        return( left, upper, right, lower )

    def left_upper( self ):
        width, height = self.width(), self.height()
        half_width, half_height = int( width / 2 ), int( height / 2 )
        left_max, upper_max = ( self.domain[0] - width ), ( self.domain[1] - height )
        left, upper = ( self.focus[0] - half_width ), ( self.focus[1] - half_height )
        left = 0 if left < 0 else \
               left_max if left > left_max else \
               left 
        upper = 0 if upper < 0 else \
                upper_max if upper > upper_max else \
                upper
        return left, upper 

    def zoom(self, delta):
        self.scale += delta
        # limit zoom to 1-90, 10=1x, 90=9x, 1=1/10x
        self.scale =         10 if self.scale <  10 else \
                            100 if self.scale > 100 else \
                     self.scale
        
    # focus should be scaled to a domain point
    def move_focus_to(self, xy):
        x, y = xy
        x_max, y_max = self.domain
        x = ( 0 if x < 0 else
              x_max - 1 if x >= x_max else
              x )
        y = ( 0 if y < 0 else
              y_max - 1 if y >= y_max else
              y )
        self.focus = ( x, y )

    def move_focus_by(self, dxdy):
        x, y = self.focus
        dx, dy = dxdy
        x, y = ( x + dx ),  (y + dy )
        # limit focus to inside viewable
        do_left, do_upper, do_right, do_lower = self.bbox()
        do_width, do_height = ( do_right - do_left ), ( do_lower - do_upper )
        do_half_width, do_half_height = int( do_width / 2 ), int( do_height / 2 ) 
        x_min, y_min = do_half_width, do_half_height
        x_max, y_max = int( self.domain[0] - do_half_width ), ( self.domain[1] - do_half_height )
        x = ( x_min if x < x_min else
              x_max - 1 if x >= x_max else
              x )
        y = ( y_min if y < y_min else
              y_max - 1 if y >= y_max else
              y )
        self.focus = ( x, y )


class ResizableCanvas(tkinter.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)


class ResizableImage(ResizableCanvas):
    def __init__(self, parent, image_name, **kwargs):
        super().__init__(parent, **kwargs)
        super().pack(fill=tkinter.BOTH, expand=tkinter.YES)
     
        self.image_original = Image.open(image_name)
        self.image = self.image_original.copy()
        self.tk_image = None

        self.scroll_origin = None
        self.zooming = False
        self.view_port = ViewPort(self.image.size)

        # Scroll - left drag
        self.bind("<Button-1>", self.on_mouse_left)
        self.bind("<B1-Motion>", self.on_mouse_move_left)
        # zoom - wheel(V), shift-wheel(H)
        self.bind("<MouseWheel>", self.on_mouse_scroll)
        #self.bind("<Shift-MouseWheel>", self.on_shift_mouse_scroll)
        self.bind("<Motion>", self.on_mouse_move)
        
    def resize(self):
        cropped_image = self.image.crop(self.view_port.bbox()) 
        resized_image = cropped_image.resize((self.width, self.height), resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.create_image(0, 0, anchor="nw", image=self.tk_image)

    def on_resize(self, event):
        super().on_resize(event)
        self.resize()

    def zoom(self, xy, zoom):
        # convert center from canvas coord (mouse) to image
        x, y = xy
        abs_x = self.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
        abs_y = self.winfo_rooty() - self.winfo_toplevel().winfo_rooty()
        xy = (x - abs_x, y - abs_y)
        xy = self.view_port.map_to_domain(xy, (0, 0, self.width, self.height))
        if not self.zooming:
            self.zooming = True
            self.view_port.move_focus_to(xy)
        self.view_port.zoom(zoom)
        self.resize()

    def scroll_start(self, xy):
        self.scroll_origin = xy

    def scroll(self, offset):
        delta = (self.scroll_origin[0] - offset[0],
                 self.scroll_origin[1] - offset[1])
        self.scroll_start(offset)
        self.view_port.move_focus_by(delta)
        self.resize()

    def on_mouse_left(self, event):
        self.zooming = False
        self.scroll_start((event.x, event.y))
    
    def on_mouse_move_left(self, event):
        self.zooming = False
        self.scroll((event.x, event.y))
    
    def on_mouse_scroll(self, event):
        # zoom with up-down movement (two finger drag)
        self.zoom((event.x, event.y), event.delta)

    def on_shift_mouse_scroll(self, event):
        # zoom with left-right movement (two finger drag)
        self.zoom((event.x, event.y), event.delta)
    
    def on_mouse_move(self, event):
        self.zooming = False


if __name__ == "__main__":
    import os
    
    here = os.path.abspath(__file__)
    image_path = os.path.join(os.path.dirname(here), "../../data/board.png")
 
    root = tkinter.Tk()
    root.title("Grid")
    root.geometry("800x600+0+0")
    # root should be configured as 'resizable' grid with 'weight'
    tkinter.Grid.rowconfigure(root, 0, weight=1)
    tkinter.Grid.columnconfigure(root, 0, weight=1)

    grid = tkinter.Frame(root)
    grid.grid(row=0, column=0, sticky="news")

    center = ResizableImage(grid, image_path, width=400, height=300,
                            bg="white", highlightthickness=0)
    center.grid(column=1, row=1, columnspan=2, rowspan=2, sticky="news")
    
    corner00 = tkinter.Canvas(grid, width=100, height=75, bg="grey", highlightthickness=0).grid(
        column=0, row=0)
    corner30 = tkinter.Canvas(grid, width=100, height=75, bg="grey", highlightthickness=0).grid(
        column=3, row=0)
    corner03 = tkinter.Canvas(grid, width=100, height=75, bg="grey", highlightthickness=0).grid(
        column=0, row=3)
    corner33 = tkinter.Canvas(grid, width=100, height=75, bg="grey", highlightthickness=0).grid(
        column=3, row=3)
    
    side_n = tkinter.Canvas(grid, width=400, height=75,  bg="green", highlightthickness=0).grid(
        column=1, row=0, columnspan=2, sticky="ew")
    side_e = tkinter.Canvas(grid, width=100, height=300, bg="green", highlightthickness=0).grid(
        column=3, row=1, rowspan=2, sticky="ns")
    side_w = tkinter.Canvas(grid, width=100, height=300, bg="green", highlightthickness=0).grid(
        column=0, row=1, rowspan=2, sticky="ns")
    side_s = tkinter.Canvas(grid, width=400, height=75,  bg="green", highlightthickness=0).grid(
        column=1, row=3, columnspan=2, sticky="ew")

    tkinter.Grid.columnconfigure(grid, tuple(range(4)), weight=1)
    tkinter.Grid.rowconfigure(grid, tuple(range(4)), weight=1)
    tkinter.Grid.columnconfigure(grid, tuple(range(1,2)), weight=4)
    tkinter.Grid.rowconfigure(grid, tuple(range(1,2)), weight=4)
    
    tkinter.mainloop()

