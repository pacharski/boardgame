import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

import json
from collections import OrderedDict
from copy import deepcopy
import board_game as bg


class Space():
    def __init__(self, id=-1, name="space", level=-1,
                       center=None, vertices=None, exits=None):
        self.id = id
        self.name = name
        self.level = level
        self.center = center
        self.vertices = vertices if vertices != None else []
        self.exits = exits if exits != None else []
        
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
        return {"__type__":  "Space",
                "id":        self.id,
                "center":    None if self.center == None else list(self.center.xy),
                "level":     self.level if self.level != None else 0,
                "name":      self.name,
                "vertices":  [list(v.xy) for v in self.vertices],
                "exits":     self.exits}
    
    # Note: this is a class function
    def json_decode(json_dict):
        space_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Space")) else
                      None)
        if space_dict != None:
            id         = space_dict["id"]
            name       = space_dict["name"]
            level      = space_dict["level"]
            center     = space_dict["center"]
            vertices   = space_dict["vertices"]
            exits      = space_dict.get("exits", [])
            return Space(id=int(id),
                         name=name,
                         level=int(level),
                         center=None if center == None else bg.Point(x=int(center[0]), y=int(center[1])),
                         vertices=[bg.Point(x=int(v[0]), y=int(v[1])) for v in vertices],
                         exits=[exit for exit in exits]
                        )
        return json_dict
    
    def __str__(self):
        form="Space: {} {} Center={} Level={}, Exits={} Vertices={}"
        return form.format(self.id, self.name, self.center, self.level,
                           self.num_exits, self.num_vertices 
                          )


class Board():
    def __init__(self, json_path=None, spaces=None, name=None):
        self.name = name if name != None else ""
        self.spaces = spaces if spaces != None else dict()
        self.last_space_id = None
        self.json_path=json_path
        if self.json_path != None:
            self.load_from_json_path(self.json_path)

    def find_space_by_location(self, id):
        return self.spaces[id]
        
    def find_space(self, point):
        x, y = point.xy
        min_dist, closest_id, closest_space = None, None, None
        for id, space in self.spaces.items():
            cx, cy = space.center.xy
            dist = ((x - cx) ** 2) + ((y - cy) ** 2)
            if (min_dist == None) or (dist < min_dist):
                min_dist = dist
                closest_id, closest_space = id, space
        return closest_id, closest_space
                
    def add_space(self, space, copy=False):
        space_id = (self.last_space_id + 1 if (self.last_space_id != None) else
                    (max(self.spaces.keys()) + 1) if (len(self.spaces.keys()) > 0) else
                    0)
        self.spaces[space_id] = space.deep_copy() if copy else space
        self.spaces[space_id].id = space_id
        self.last_space_id = space_id

    def __str__(self):
        form = "Board: Spaces={}"
        return form.format(len(self.spaces))
    
    def __len__(self):
        return len(self.spaces) 
        
    def json_encode(self):
        sorted_keys = sorted([int(k) for k in self.spaces.keys()])
        sorted_spaces = OrderedDict()
        for k in sorted_keys:
            sorted_spaces[k] = self.spaces[k]
        return {"__type__":  "Board",
                "name":      self.name,
                "spaces":    sorted_spaces
               } 
    
    # Note: this is a class function
    def json_decode(json_dict):
        board_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Board")) else
                      None)
        if board_dict != None:
            name = board_dict.get("name", None)
            spaces = board_dict["spaces"]
            spaces = {int(k): v for k, v in spaces.items()}
            for k, v in spaces.items():
                if v.id < 0:
                    v.id = int(k)
            return Board(name=name, spaces=spaces)
        return json_dict
        
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": bg.Space,
                                    "Point": bg.Point, "Exit": bg.Exit})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": bg.Space,
                                    "Point": bg.Point, "Exit": bg.Exit})    
        json_path = json_path if json_path != None else self.json_path
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            if isinstance(json_data, dict):
                self.spaces = {int(k): v for k, v in json_data.get("spaces", {}).items()}
                for k, v in self.spaces.items():
                    if v.id < 0:
                        v.id = int(k)
                self.last_space_id = None
            else:
                self.name = json_data.name
                self.spaces = json_data.spaces
                self.last_space_id = json_data.last_space_id
                self.json_path = json_data.json_path if json_data.json_path != None else self.json_path
        except Exception as e:
            print("\nException (Board.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Board(json_path=json_path)


if __name__ == "__main__":
    print(Board())
    
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    print("\n\n\nMainHere", here)
    json_path = os.path.join(here, "../../data/board.json")
    print(Board(json_path=json_path))
