from copy import deepcopy

from point import Point


class Space():
    def __init__(self, id=-1, name="space", level=-1,
                       center=None, vertices=[], exits=[] ):
        
        self.id = id
        self.name = name
        self.level = level
        self.center = center
        self.vertices = vertices
        self.exits = exits

    def reset(self):
        self.id = -1
        self.name = ""
        self.level = -1
        self.center = None
        self.vertices = []
        self.exits = []
        
    def add_vertex(self, point):
        self.vertices.append(point)

    def remove_last_vertex(self):
        self.vertices = self.vertices[:-1]

    def deep_copy(self):
        return deepcopy(self)

    @property
    def num_vertices(self):
        return len(self.vertices)
    
    def add_exit(self, exit):
        self.exits.append(exit)

    @property
    def num_exits(self):
        return len(self.exits)
    
    def json_encode(self):
        return { "Space": { "id": self.id,
                            "center": None if self.center == None else list(self.center.xy),
                            "level": self.level if self.level != None else 0,
                            "name": self.name,
                            "vertices": [list(v.xy) for v in self.vertices],
                            "exits": self.exits } }
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Space" in json_dict:
            id = json_dict["Space"]["id"]
            name = json_dict["Space"]["name"]
            level = json_dict["Space"]["level"]
            center = json_dict["Space"]["center"]
            vertices = json_dict["Space"]["vertices"]
            exits = json_dict["Space"].get("exits", [])
            return Space(id=int(id),
                         name=name,
                         level=int(level),
                         center=None if center == None else Point(x=int(center[0]), y=int(center[1])),
                         vertices=[Point(x=int(v[0]), y=int(v[1])) for v in vertices],
                         exits=[exit for exit in exits]
                        )
    
    def __str__(self):
        form="Space {id}:  Name={name} Center={center} Level={level}, Exits={exits} Vertices={sides}"
        return form.format(id=self.id, name=self.name, 
                           center=self.center, level=self.level,
                           exits=self.num_exits, 
                           sides=self.num_vertices 
                          )
    
    
import json 
if __name__ == "__main__":
    class SpaceEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Space):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
        
    class SpaceDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Space' in dct:
                return Space.json_decode(dct)
            return dct

    s1 = Space()
    s2 = Space(id=2, name="Crypt", center=Point(5, 6), level=4)
    s3 = Space(id=3, name="Queen's Crypt", center=Point(5, 6), level=4)
    s3.vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)]
    s4 = Space(name="Queen's Crypt", center=Point(5, 6), level=4,
               vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)])
    s4.add_vertex(Point(7,8))
    s5 = s4.deep_copy()
    s5.add_vertex(Point(11,12))
    
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print()

    spaces = [s1, s2, s3, s4, s5]
    
    filename = "temp/space.json"
    with open(filename, 'w') as jsonfile:
        json.dump(spaces, jsonfile, cls=SpaceEncoder)
    with open(filename, 'r') as jsonfile:
        spaces_copy = json.load(jsonfile, cls=SpaceDecoder)
    assert len(spaces) == len(spaces_copy)
    for idx in range(len(spaces)):
        print("{} == {}".format(spaces[idx], spaces_copy[idx]))
        assert spaces[idx].name  == spaces_copy[idx].name
        assert spaces[idx].level == spaces_copy[idx].level

    print()
    for _ in range(10):
        s4.remove_last_vertex()
        print(s4)
