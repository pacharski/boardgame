import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

from copy import deepcopy
import board_game as bg
#import fafo as ff


class Space(bg.Space):
    def __init__(self, id=-1, name="space", level=-1,
                       center=None, vertices=None, exits=None, 
                       distance_from_end=None ):
        super().__init__(id=id, name=name, level=level, 
                         center=center, vertices=vertices, exits=exits)
        self.distance_from_end = distance_from_end
        
    def reset(self):
        super().reset()
        self.distance_from_end = None
        
    def deep_copy(self):
        return deepcopy(self)

    def json_encode(self):
        return {"__type__":  "Space",
                "id":                self.id,
                "center":            None if self.center == None else list(self.center.xy),
                "level":             self.level if self.level != None else 0,
                "name":              self.name,
                "vertices":          [list(v.xy) for v in self.vertices],
                "exits":             self.exits,
                "distance_from_end": self.distance_from_end}
    
    # Note: this is a class function
    def json_decode(json_dict):
        space_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Space")) else
                      None)
        if space_dict != None:
            id                = space_dict["id"]
            name              = space_dict["name"]
            level             = space_dict["level"]
            center            = space_dict["center"]
            vertices          = space_dict["vertices"]
            exits             = space_dict.get("exits", [])
            distance_from_end = space_dict.get("distance_from_end", None)
            return Space(id=int(id),
                         name=name,
                         level=int(level),
                         center=None if center == None else bg.Point(x=int(center[0]), y=int(center[1])),
                         vertices=[bg.Point(x=int(v[0]), y=int(v[1])) for v in vertices],
                         exits=[exit for exit in exits],
                         distance_from_end=distance_from_end
                        )
        return json_dict
    
    def __str__(self):
        form="Space: {} {} Center={} Level={}, Exits={} ToEnd={} Vertices={}"
        return form.format(self.id, self.name, self.center, self.level,
                           self.num_exits, self.distance_from_end, self.num_vertices 
                          )


if __name__ == "__main__":
    print(Space())