
from PIL import Image, ImageTk
import tkinter

class LayoutBbox():
    def __init__(self, bbox):
        """bbox is defined in mils of the overall layout"""
        self.bbox = bbox
    
    def scale_to_bbox(self, bbox):
        print("ScaleBbox(bb)")
        left, upper, right, lower = bbox
        width = right - left
        height = lower - upper
        s_left, s_upper, s_right, s_lower = self.scale_to_width_and_height(width, height)
        return (left + s_left, upper + s_upper, left + s_right, upper + s_lower)

    def scale_to_width_and_height(self, width, height):
        """No negative numbers, so use int() instead of math.floor()"""
        print("ScaleBbox(wh)")
        left, upper, right, lower = self.bbox
        return (int((height * left)  / 1000),
                int((width  * upper) / 1000),
                int((height * lower) / 1000), 
                int((width  * right) / 1000))
        

class LayoutBlock():
    def __init__(self, name, item, layout_bbox: LayoutBbox):
        """bbox is defined in mils of the overall layout"""
        self.name = name
        self.item = item
        self.layout_bbox = layout_bbox
    
    def scale_to_bbox(self, bbox):
        print("ScaleBlock(bb)")
        return self.layout_bbox.scale_to_bbox(bbox)
        
    def scale_to_width_and_height(self, width, height):
        print("ScaleBlock(wh)")
        return self.layout_bbox.scale_to_width_and_height(width, height)
    

class LayoutProportional():
    """Simple layout manager that manages a set of blocks and scales everything proportionally"""
    def __init__(self, blocks=None):
        self.blocks = dict() if blocks == None else blocks
        
    def scale_to_bbox(self, bbox):
        """Scale everything and return a dict of tuple.
           Should not need to snap because the edges should calculate the 
            same scaled value given the same input value
        """
        return {key: (block.name, block.item, block.scale_to_bbox(bbox)) 
                for key, block in self.blocks.items()}
    
    def scale_to_width_and_height(self, width, height):
        """Scale everything, and return as a dict of tuple.
           Should not need to snap because the edges should calculate the 
            same scaled value given the same input value
        """
        return {key: (block.name, block.item, block.scale_to_width_and_height(width, height)) 
                for key, block in self.blocks.items()}
    

class ProportionalFrame(tkinter.Frame):
    def __init__(self, parent, layout=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.bind("<Configure>", self.on_resize)

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self._layout = layout
        
    # layout is private with setter/getter so an action can be taken on set
    @property
    def layout(self):
        return self._layout
    
    @layout.setter
    def layout(self, value):
        """Set the layout and redraw?"""
        self._layout = value if value != None else LayoutProportional()

    @layout.deleter
    def layout(self):
        del self._layout

    def resize(self):
        print("PropFrame.resize")
        # if self.layout != None:
        #     scaled_layout = self.layout.scale_to_width_and_height(self.width, self.height)
        #     for key, layout in scaled_layout.items():
        #         name, item, bbox = layout
        #         left, upper, _, _ = bbox
        #         print("Place", key, name, item, bbox)
        #         item.place(x=left, y=upper)
        #label1 = tkinter.Label(self, text="This is a label")
        # label1.image = bardejov
        #label1.place(x=20, y=20)
        
    def on_resize(self, event):
        """Redraw everything scaled to the new hight and width"""
        print("PropFrame.on_resize")
        #super().on_resize(event)
        self.width = event.width
        self.height = event.height
        #self.resize()


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


class FixedSizeImage(tkinter.Canvas):
    def __init__(self, parent, image_name, **kwargs):
        super().__init__(parent, **kwargs)
        #super().pack(fill=tkinter.BOTH, expand=tkinter.YES)
     
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
    root.title("ProportionalCanvas")
    root.geometry("800x600+0+0")
    tkinter.Grid.rowconfigure(root, 0, weight=1)
    tkinter.Grid.columnconfigure(root, 0, weight=1)

    #Create & Configure frame 
    prop_frame=tkinter.Frame(root)
    prop_frame.grid(row=0, column=0, sticky="news")
    
    board_canvas = ResizableImage(prop_frame, image_path, width=400, height=300,
                                  bg="white", highlightthickness=0)
    board_canvas.grid(column=1, row=1, columnspan=2, rowspan=2,
                      sticky="news")
    tkinter.Grid.columnconfigure(prop_frame, tuple(range(1,2)), weight=1)
    tkinter.Grid.rowconfigure(prop_frame, tuple(range(1,2)), weight=1)
    
    #board_canvas.pack()
    #board_canvas.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
    label00 = tkinter.Label(prop_frame, text="Label00").grid(
               column=0, row=0)
    label30 = tkinter.Label(prop_frame, text="Label30").grid(
               column=3, row=0)
    label03 = tkinter.Label(prop_frame, text="Label03").grid(
               column=0, row=3)
    label33 = tkinter.Label(prop_frame, text="Label33").grid(
               column=3, row=3)
    
    # layout = LayoutProportional({"Board": 
    #                              LayoutBlock("Board", board_canvas, LayoutBbox((200, 200, 300, 300))),
    #                              "Label2": 
    #                              LayoutBlock("Label2", label2, LayoutBbox((100, 100, 200, 200)))
    #                            })
    # prop_frame.layout = layout     

    """Achieving the same result using place is much harder because it accepts highly hard
       coded values", incorrect remark "relheight, relwidth − Height and width as a float 
       between 0.0 and 1.0, as a fraction of the height and width of the parent widget
       . relx, rely − Horizontal and vertical offset as a float between 0.0 and 1.0, as a 
       fraction of the height and width of the parent widget."""

    tkinter.mainloop()

