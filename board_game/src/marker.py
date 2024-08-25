# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())


class Marker():
    cShapes = ["circle", "triangle", "square", "pentagon", "hexagon",
               "star"]
    
    def __init__(self, color=None, shape=None, size=None,
                 name=None, image_path=None, image=None):
        self.color = color
        self.shape = shape
        self.size = size
        self.name = name
        self.image_path = image_path
        self.image = image
        
    def __str__(self):
        form = "Marker: {name}Shape={color}-{shape}-{size} Image={image}"
        return form.format(name=((self.name + " ") if isinstance(self.name, str) else ""),
                           color=self.color, shape=self.shape, 
                           size=("auto" if self.size == None else self.size),
                           image=self.image_path)
    
    def json_encode(self):
        return {"__type__":    "Marker",
                "color":       self.color,
                "shape":       self.shape,
                "size":        self.size,
                "name":        self.name,
                "image_path":  self.image_path
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        # marker_dict = (json_dict["Marker"] if "Marker" in json_dict else
        marker_dict = (json_dict if ("__type__" in json_dict) and (json_dict["__type__"] == "Marker") else
                       None)
        if marker_dict != None:
            color      = marker_dict["color"]
            shape      = marker_dict["shape"]
            size       = marker_dict["size"]
            name       = marker_dict["name"]
            image_path = marker_dict["image_path"]
            return Marker(color=color,
                          shape=shape,
                          size=int(size) if size != None else size,
                          name=name,
                          image_path=image_path
                         )
        

if __name__ == '__main__':
    t1 = Marker("green",   "square", name="G-er") 
    t2 = Marker( "blue",   "circle", name="B-er") 
    t3 = Marker(  "red", "triangle", name="R-er")  
    t4 = Marker(  "red", "triangle", name="R-er")   
    t5 = Marker("white",     "star", name="W-er")

    markers = [t1, t2, t3, t4, t5]
    for marker in markers:
        print(marker)