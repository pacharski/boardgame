import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

import json
from collections import OrderedDict
import board_game as bg
import fafo as ff


class Board(bg.Board):
    def __init__(self, json_path=None, spaces=None, name=None):
        super().__init__(json_path=json_path, spaces=spaces, name=name)
        
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": ff.Space,
                                    "Point": bg.Point, "Exit": bg.Exit})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": Board, "Space": ff.Space,
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

    
if __name__ == "__main__":
    print(Board())
    
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    print("\n\n\nMainHere", here)
    json_path = os.path.join(here, "../../data/board.json")
    print(Board(json_path=json_path))
