# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
from copy import deepcopy

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))
import board_game as bg


class Space():
    def __init__(self, id=-1, name="space", level=-1,
                       center=None, vertices=None, exits=None, encounters=None ):
        self.id = id
        self.name = name
        self.level = level
        self.center = center
        self.vertices = vertices if vertices != None else []
        self.exits = exits if exits != None else []
        self.encounters = encounters if encounters != None else []

    def reset(self):
        self.id = -1
        self.name = ""
        self.level = -1
        self.center = None
        self.vertices = []
        self.exits = []
        self.encounters = []
        
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
    
    @property
    def num_encounters(self):
        return len(self.encounters)
    
    def json_encode(self):
        return {"__type__":  "Space",
                "id":        self.id,
                "center":    None if self.center == None else list(self.center.xy),
                "level":     self.level if self.level != None else 0,
                "name":      self.name,
                "vertices":  [list(v.xy) for v in self.vertices],
                "exits":     self.exits,
                "encounter": self.encounters}
    
    # Note: this is a class function
    def json_decode(json_dict):
        space_dict = (json_dict["Space"] if ("Space" in json_dict) else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Space")) else
                      None)
        if space_dict != None:
            id         = space_dict["id"]
            name       = space_dict["name"]
            level      = space_dict["level"]
            center     = space_dict["center"]
            vertices   = space_dict["vertices"]
            exits      = space_dict.get("exits", [])
            encounters = space_dict.get("encounters", [])
            return Space(id=int(id),
                         name=name,
                         level=int(level),
                         center=None if center == None else bg.Point(x=int(center[0]), y=int(center[1])),
                         vertices=[bg.Point(x=int(v[0]), y=int(v[1])) for v in vertices],
                         exits=[exit for exit in exits],
                         encounters=encounters
                        )
        return json_dict
    
    def __str__(self):
        form="Space: {} {} Center={} Level={}, Exits={} Encounters={} Vertices={}"
        return form.format(self.id, self.name, self.center, self.level,
                           self.num_exits, self.num_encounters, self.num_vertices 
                          )


if __name__ == "__main__":
    print(Space())