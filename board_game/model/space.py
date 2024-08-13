# organization is package/module/submodule
import setup
from board_game.model.point import Point

from copy import deepcopy


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
        return { "Space": { "id":       self.id,
                            "center":   None if self.center == None else list(self.center.xy),
                            "level":    self.level if self.level != None else 0,
                            "name":     self.name,
                            "vertices": [list(v.xy) for v in self.vertices],
                            "exits":    self.exits } }
    
    # Note: this is a class function
    def json_decode(json_dict):
        space_dict = (json_dict["Space"] if ("Space" in json_dict) else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Space")) else
                      None)
        if space_dict != None:
            id       = space_dict["id"]
            name     = space_dict["name"]
            level    = space_dict["level"]
            center   = space_dict["center"]
            vertices = space_dict["vertices"]
            exits    = space_dict.get("exits", [])
            return Space(id=int(id),
                         name=name,
                         level=int(level),
                         center=None if center == None else Point(x=int(center[0]), y=int(center[1])),
                         vertices=[Point(x=int(v[0]), y=int(v[1])) for v in vertices],
                         exits=[exit for exit in exits]
                        )
        return json_dict
    
    def __str__(self):
        form="Space {id}:  Name={name} Center={center} Level={level}, Exits={exits} Vertices={sides}"
        return form.format(id=self.id, name=self.name, 
                           center=self.center, level=self.level,
                           exits=self.num_exits, 
                           sides=self.num_vertices 
                          )
    

if __name__ == "__main__":
    print(Space())
    print(Space(0, "Well lit Chamber", 0))
