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
        return {"Marker": {"name": self.name,
                          "color": self.color,
                          "shape": self.shape,
                          "size": self.size,
                          "image_path": self.image_path}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Marker" in json_dict:
            name       = json_dict["Marker"]["name"]
            color      = json_dict["Marker"]["color"]
            shape      = json_dict["Marker"]["shape"]
            size       = json_dict["Marker"]["size"]
            image_path = json_dict["Marker"]["image_path"]
            return Marker(name=name,
                         color=color,
                         shape=shape,
                         size=int(size) if size != None else size,
                         image_path=image_path
                        )
        

if __name__ == '__main__':
    import os
    import json
    from json_encoder import CompactJSONEncoder

    class LocalEncoder(CompactJSONEncoder):
        def default(self, o):
            if isinstance(o, Marker):
                return o.json_encode()
            return CompactJSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if "Marker" in dct:
                return Marker.json_decode(dct)
            return dct
        
    t1 = Marker("G-er", "green", "square") 
    t2 = Marker("B-er", "blue",  "circle") 
    t3 = Marker("R-er", "red",   "triangle")  
    t4 = Marker("R-er", "red",   "triangle")   
    t5 = Marker("W-er", "white", "star")

    markers = [t1, t2, t3, t4, t5]
    for marker in markers:
        print(marker)

    filename = "temp/marker.json"
    with open(filename, 'w') as jsonfile:
        json.dump(markers, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        markers_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(markers) == len(markers_copy)
    assert markers[0].name == markers_copy[0].name
