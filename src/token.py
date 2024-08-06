class Token():
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
        form = "Token: {} Shape={}-{}-{} Image={}"
        return form.format(self.name, self.color, self.shape, 
                           "auto" if self.size == None else self.size,
                           self.image_path)
    
    def json_encode(self):
        return {"Token": {"name": self.name,
                          "color": self.color,
                          "shape": self.shape,
                          "size": self.size,
                          "image_path": self.image_path}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Token" in json_dict:
            name       = json_dict["Token"]["name"]
            color      = json_dict["Token"]["color"]
            shape      = json_dict["Token"]["shape"]
            size       = json_dict["Token"]["size"]
            image_path = json_dict["Token"]["image_path"]
            return Token(name=name,
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
            if isinstance(o, Token):
                return o.json_encode()
            return CompactJSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if "Token" in dct:
                return Token.json_decode(dct)
            return dct
        
    t1 = Token("G-er", "green", "square") 
    t2 = Token("B-er", "blue", "circle") 
    t3 = Token("R-er", "red", "triangle")  
    t4 = Token("R-er", "red", "triangle")   
    t5 = Token("W-er", "white", "star")

    tokens = [t1, t2, t3, t4, t5]
    for token in tokens:
        print(token)

    filename = "temp/token.json"
    with open(filename, 'w') as jsonfile:
        json.dump(tokens, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        tokens_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(tokens) == len(tokens_copy)
    assert tokens[0].name == tokens_copy[0].name
