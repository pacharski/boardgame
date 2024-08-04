from enum import IntEnum


class Path():
    class Type(IntEnum):
        cClear      = 0
        cDoor       = 1
        cSecretDoor = 2
        cImpasse    = 3

    def type_name(int_type):
        return ("Blocked"     if int_type == Path.Type.cImpasse else
                "Door"        if int_type == Path.Type.cDoor else
                "Secret Door" if int_type == Path.Type.cSecretDoor else
                "")

    def __init__(self, name="", origin=None, terminus=None,
                       forward=Type.cClear, backward=Type.cClear):
        self.name      = name
        self.origin    = origin
        self.terminus  = terminus
        self.forward   = forward
        self.backward  = backward

    def reset(self):
        self.name = ""
        self.origin = None 
        self.terminus = None
        self.forward = Path.Type.cClear 
        self.backward = Path.Type.cClear

    def __str__(self):
        types = ["-", "D", "S", "|"]
        form = "Path {name}:  {origin} <{backward}--{forward}> {terminus}"
        return form.format(name=self.name, origin=self.origin, terminus=self.terminus,
                           forward=types[self.forward], backward=types[self.backward]
                          )
    
    def json_encode(self):
        return { "Path": { "name":     self.name,
                           "origin":   self.origin,
                           "terminus": self.terminus,
                           "forward":  self.forward,
                           "backward": self.backward
                         } }
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Path" in json_dict:
            name      = json_dict["Path"]["name"]
            origin    = json_dict["Path"]["origin"]
            terminus  = json_dict["Path"]["terminus"]
            forward   = json_dict["Path"]["forward"]
            backward  = json_dict["Path"]["backward"]
            return Path(name=name,
                        origin=int(origin),
                        terminus=int(terminus),
                        forward=int(forward),
                        backward=int(backward)
                       )
    
    
import json 
if __name__ == "__main__":
    class PathEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Path):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
        
    class PathDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Path' in dct:
                return Path.json_decode(dct)
            return dct

    c1 = Path()
    c1.name = "c1"
    c1.origin=11
    c1.terminus=71
    c1.forward = c1.backward = Path.Type.cSecretDoor

    c2 = Path(name="c2", origin=13, terminus=23)
    c2.forward = Path.Type.cDoor

    c3 = Path(name="c3", origin=13, terminus=23)
    c3.backward = Path.Type.cImpasse

    print(c1)
    print(c2)
    print(c3)
 
    paths = [c1, c2, c3]
    filename = "path.json"
    with open(filename, 'w') as jsonfile:
        json.dump(paths, jsonfile, cls=PathEncoder)
    with open(filename, 'r') as jsonfile:
        paths_copy = json.load(jsonfile, cls=PathDecoder)
    assert len(paths) == len(paths_copy)
    for idx in range(len(paths)):
        print("{} == {}".format(paths[idx], paths_copy[idx]))
        assert paths[idx].name  == paths_copy[idx].name
        print("{} == {}".format(paths[idx].origin, paths_copy[idx].origin))
        print("{} == {}".format(type(paths[idx].origin), type(paths_copy[idx].origin)))
        assert paths[idx].origin == paths_copy[idx].origin
        assert paths[idx].terminus == paths_copy[idx].terminus
        assert paths[idx].forward == paths_copy[idx].forward
        assert paths[idx].backward == paths_copy[idx].backward
    