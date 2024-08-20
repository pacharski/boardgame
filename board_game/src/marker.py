# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())


class Marker():
    cShapes = ["circle", "triangle", "square", "pentagon", "hexagon",
               "star"]
    
    def __init__(self, name, color=None, shape="circle", size=None,
                 image_path=None, image=None):
        self.name = name
        self.color = color
        self.shape = shape
        self.size = size
        self.image_path = image_path
        self.image = image
        
    def __str__(self):
        form = "Marker: {} Shape={}-{}-{} Image={}"
        return form.format(self.name, self.color, self.shape, 
                           "auto" if self.size == None else self.size,
                           self.image_path)
    
    def json_encode(self):
        return {"__type__":    "Marker",
                "name":        self.name,
                "color":       self.color,
                "shape":       self.shape,
                "size":        self.size,
                "image_path":  self.image_path
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        marker_dict = (json_dict["Marker"] if "Marker" in json_dict else
                       json_dict if ("__type__" in json_dict) and (json_dict["__type__"] == "Marker") else
                       None)
        if marker_dict != None:
            name       = marker_dict["name"]
            color      = marker_dict["color"]
            shape      = marker_dict["shape"]
            size       = marker_dict["size"]
            image_path = marker_dict["image_path"]
            return Marker(name=name,
                         color=color,
                         shape=shape,
                         size=int(size) if size != None else size,
                         image_path=image_path
                        )
        

if __name__ == '__main__':
    t1 = Marker("G-er", "green", "square") 
    t2 = Marker("B-er", "blue",  "circle") 
    t3 = Marker("R-er", "red",   "triangle")  
    t4 = Marker("R-er", "red",   "triangle")   
    t5 = Marker("W-er", "white", "star")

    markers = [t1, t2, t3, t4, t5]
    for marker in markers:
        print(marker)