# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
import json
from collections import OrderedDict

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))
import board_game as bg

#import sys
#print("SysPath2:", "\n\t".join([""] + [str(p) for p in sys.path]))

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
        #board_dict = (json_dict["Board"] if ("Board" in json_dict) else
        board_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Board")) else
                      None)
        if board_dict != None:
            #if isinstance(board_dict, dict):
            # print("\nGetName", type(board_dict), board_dict.keys())
            name = board_dict.get("name", None)
            spaces = board_dict["spaces"]
            spaces = {int(k): v for k, v in spaces.items()}
            for k, v in spaces.items():
                if v.id < 0:
                    v.id = int(k)
            return Board(name=name, spaces=spaces)
            # else:
            #     print("\nAlreadyIsBoard", type(board_dict))
            #     return board_dict # should already be Board type
        return json_dict
        
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": bg.Space,
                                   "Point": bg.Point, "Path": Path, "Exit": bg.Exit})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": bg.Space,
                                   "Point": bg.Point, "Path": Path, "Exit": bg.Exit})    
        json_path = json_path if json_path != None else self.json_path
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            if isinstance(json_data, dict):
                # print("\nBoard.load_from_json_path", json_data.keys())
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
        return Board(json_path)


if __name__ == "__main__":
    print(Board())
    
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    print("\n\n\nMainHere", here)
    json_path = os.path.join(here, "../../data/board.json")
    print(Board(json_path=json_path))

#     here = os.path.abspath(__file__)
#     json_path = os.path.join(os.path.dirname(here), "../../data/board.json" )

#     board = Board(json_path)
#     print("CWD", os.getcwd())
#     temp_path = os.path.join(os.path.dirname(here), "board.json")
#     board.save_to_json_path(temp_path)
#     board1 = Board(temp_path)
#     board2 = Board.from_json_path(temp_path)

#     print(board1)
#     assert len(board1.spaces) == len(board2.spaces)
#     assert len(board1.spaces) == 419
#     assert len(board1) == 419
    
#     print("Find(100,100)", board1.find_space(Point(100, 100)))
#     assert board1.find_space(Point(100, 100))[0] == 333
#     print("Find(200,100)", board1.find_space(Point(200, 100)))
#     assert board1.find_space(Point(200, 100))[0] == 329
