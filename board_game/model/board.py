import os
import json
from collections import OrderedDict

from json_encoder import CompactJSONEncoder
from point import Point
from space import Space
from path import Path
from exit import Exit


class Board():
    def __init__(self, json_path=None, spaces=dict()):
        self.spaces = spaces
        self.last_space_id = None
        self.json_path=json_path
        if self.json_path != None:
            self.load_from_json_path(self.json_path)
        
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
                    max(self.spaces.keys()) + 1)
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
        return {"spaces": sorted_spaces
               } 
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Board" in json_dict:
            spaces = json_dict["Board"]["spaces"]
            return Board(spaces=spaces)
        
    def save_to_json_path(self, json_path=None):
        class LocalJSONEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, (Board, Space, Point, Path, Exit)):  
                    return o.json_encode()
                return CompactJSONEncoder.default(self, o)
        
        json_path = json_path if json_path != None else self.json_path
        print("SaveToFile", json_path)
        
        with open(json_path, 'w') as json_file:
                  json.dump(self, json_file, indent=2, sort_keys=False,
                            cls=LocalJSONEncoder, ensure_ascii = False)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        class LocalJSONDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if 'Board' in dct:
                    return Board.json_decode(dct)
                if 'Point' in dct:
                    return Point.json_decode(dct)
                if 'Space' in dct:
                    return Space.json_decode(dct)
                if 'Path' in dct:
                    return Path.json_decode(dct)
                if 'Exit' in dct:
                    return Exit.json_decode(dct)
                return dct
            
        try:
            json_path = json_path if json_path != None else self.json_path
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, cls=LocalJSONDecoder)
            self.spaces = {int(k): v for k, v in json_data.get("spaces", {}).items()}
            for k, v in self.spaces.items():
                if v.id < 0:
                    v.id = int(k)
            self.last_space_id = None
        except Exception as e:
            print("Exception (Board.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Board(json_path)


if __name__ == "__main__":
    here = os.path.abspath(__file__)
    json_path = os.path.join(os.path.dirname(here), "../../data/board.json" )

    board = Board(json_path)
    board.save_to_json_path(json_path="temp/board.json")
    board1 = Board("temp/board.json")
    board2 = Board.from_json_path("temp/board.json")

    print(board1)
    assert len(board1.spaces) == len(board2.spaces)
    assert len(board1.spaces) == 419
    assert len(board1) == 419
    
    print("Find(100,100)", board1.find_space(Point(100, 100)))
    assert board1.find_space(Point(100, 100))[0] == 333
    print("Find(200,100)", board1.find_space(Point(200, 100)))
    assert board1.find_space(Point(200, 100))[0] == 329
