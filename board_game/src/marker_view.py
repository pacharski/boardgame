from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import board_game as bg


class MarkerView():
    """Knows how to draw a Marker on a tkinter canvas"""
    def __init__(self, marker):
        self.marker = marker
        
    def __str__(self):
        form = "MarkerView: {}"
        return form.format(self.marker) 
    
    def size(self, scale=1.0):
        size = self.marker.size if self.marker.size != None else 10
        return int(size * scale)
    
    @property
    def color(self):
        return self.marker.color

    def draw(self, canvas, xy, scale=1.0):
        if self.marker.shape == "square":
            self.draw_square(canvas, xy, scale)
        elif self.marker.shape == "circle":
            self.draw_circle(canvas, xy, scale)
        elif self.marker.shape == "triangle":
            self.draw_triangle(canvas, xy, scale)
        elif self.marker.shape == "star":
            self.draw_star(canvas, xy, scale)
        else:  
            self.draw_pawn(canvas, xy, scale)

    def draw_pawn(self, canvas, xy, scale):
        # xy should already be mapped to visible(?)
        x, y = xy # self.view_port.map_to_visible(point.xy, visible_bbox)
        size = self.size(scale)
        left, right = x - size, x + size
        upper, lower = y - size, y + size
        r_head = int(size / 3)
        peak = upper + r_head
        vertices = [x, peak, left, lower, right, lower]
        canvas.create_polygon(vertices,
                              outline=self.color, fill=self.color, width=1)
        canvas.create_oval(x-r_head, peak-r_head, x+r_head, peak+r_head, 
                           outline=self.color, fill=self.color, width=1)
    
    def draw_star(self, canvas, xy, scale):
        # xy should already be mapped to visible(?)
        x, y = xy # self.view_port.map_to_visible(point.xy, visible_bbox)
        size = self.size(scale)
        left, right = x - size, x + size
        upper, lower = y - size, y + size
        r_head = int(size / 2)
        hi = upper + r_head
        lo = lower - r_head
        vertices = [x, upper, right, lo, left, lo]
        vertices_inverted = [x, lower, right, hi, left, hi]
        canvas.create_polygon(vertices, 
                              outline=self.color, fill=self.color, width=1)
        canvas.create_polygon(vertices_inverted,
                              outline=self.color, fill=self.color, width=1)
    
    def draw_triangle(self, canvas, xy, scale):
        # xy should already be mapped to visible(?)
        x, y = xy # self.view_port.map_to_visible(point.xy, visible_bbox)
        size = self.size(scale)
        left, right = x - size, x + size
        upper, lower = y - size, y + size
        vertices = [x, upper, right, lower, left, lower]
        canvas.create_polygon(vertices, 
                              outline=self.color, fill=self.color, width=1)
    
    def draw_square(self, canvas, xy, scale):
        # xy should already be mapped to visible(?)
        x, y = xy # self.view_port.map_to_visible(point.xy, visible_bbox)
        size = self.size(scale)
        left, right = x - size, x + size
        upper, lower = y - size, y + size
        canvas.create_rectangle(left, upper, right, lower, 
                                outline=self.color, fill=self.color, width=1)
    
    def draw_circle(self, canvas, xy, scale):
        # xy should already be mapped to visible(?)
        x, y = xy # self.view_port.map_to_visible(point.xy, visible_bbox)
        size = self.size(scale)
        canvas.create_oval(x-size, y-size, x+size, y+size, 
                           outline=self.color, fill=self.color, width=1)
        

if __name__ == '__main__':      
    t1 = bg.Marker("G-er", "green", "square") 
    t2 = bg.Marker("B-er", "blue",  "circle") 
    t3 = bg.Marker("R-er", "red",   "triangle")  
    t4 = bg.Marker("R-er", "red",   "triangle")   
    t5 = bg.Marker("W-er", "white", "star")

    # Display Marker on a tkinter canvas
    markers = [t1, t2, t3, t4, t5]
    marker_views = [MarkerView(marker) for marker in markers]
    for marker_view in marker_views:
        print(marker_view)
