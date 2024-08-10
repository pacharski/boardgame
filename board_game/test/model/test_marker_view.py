from marker import Marker

class MarkerView():
    """Knows how to draw a Marker on a tkinter canvas"""
    def __init__(self, marker):
        self.marker = marker
        
    def __str__(self):
        form = "MarkerView: {}"
        return form.format(self.marker)   


if __name__ == '__main__':      
    t1 = Marker("G-er", "green", "square") 
    t2 = Marker("B-er", "blue",  "circle") 
    t3 = Marker("R-er", "red",   "triangle")  
    t4 = Marker("R-er", "red",   "triangle")   
    t5 = Marker("W-er", "white", "star")

    # Display Marker on a tkinter canvas
    markers = [t1, t2, t3, t4, t5]
    marker_views = [MarkerView(marker) for marker in markers]
    for marker_view in marker_views:
        print(marker_view)
