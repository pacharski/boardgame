import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

import json
from collections import OrderedDict
import board_game as bg


class Space(bg.Space):
    def __init__(self, id=-1, name="space", level=-1,
                       center=None, vertices=None, exits=None,
                       encounters=None):
        super().__init__(id=id, name=name, level=level,
                         center=center, vertices=vertices, exits=exits)
        self.encounters = encounters if encounters != None else []
        
        
    def reset(self):
        super().reset()
        self.encounters = []
        
    @property
    def num_encounters(self):
        return len(self.encounters)
    
    def json_encode(self):
        return {"__type__":   "Space",
                "id":         self.id,
                "center":     None if self.center == None else list(self.center.xy),
                "level":      self.level if self.level != None else 0,
                "name":       self.name,
                "vertices":   [list(v.xy) for v in self.vertices],
                "exits":      self.exits,
                "encounters": self.encounters}
    
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
        form="Space: {} {} Center={} Level={}, Exits={} Vertices={} encounters={}"
        return form.format(self.id, self.name, self.center, self.level,
                           self.num_exits, self.num_vertices,
                           self.num_encounters 
                          )


class Board(bg.Board):
    def __init__(self, json_path=None, spaces=None, name=None):
        super().__init__(json_path=json_path, spaces=spaces, name=name)
        
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": Space,
                                    "Point": bg.Point, "Exit": bg.Exit})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": Space,
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
    print("Path", json_path)
    print(Board(json_path=json_path))
