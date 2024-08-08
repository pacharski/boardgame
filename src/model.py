import os
import json
from collections import OrderedDict
from enum import IntEnum
#from copy import deepcopy

from json_encoder import CompactJSONEncoder


class Point():
    """Hold an x,y pair with json encode/decode"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)
    
    def deep_copy(self):
        return deepcopy(self)
    
    def __str__(self):
        form = "Point: ({x}, {y})"
        return form.format(x=self.x, y=self.y)
    
    def json_encode(self):
        return { "Point": self.xy }
    
    def json_decode(json_dict):
        if "Point" in json_dict:
            xy = json_dict["Point"]
            return Point(x=int(xy[0]), y=int(xy[1]))


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
    

class Path():
    """Represents a connection between two spaces separated by a barrier
       With json encode/decode
    """
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
        

class Exit():
    cBarriers = ["", "Door", "Secret Door"]
    
    def __init__(self, name="", destination=None, barrier="", open=set()):
        self.name        = name
        self.destination = destination
        self.barrier     = barrier
        self.open        = open # per player (for secrect doors)
        
    def reset(self):
        self.name = ""
        self.destination = None
        self.barrier = "" 
        self.open = set() # per player

    def deep_copy(self):
        return deepcopy(self)
        
    def __str__(self):
        barrier_width = max([len(b) for b in Exit.cBarriers])
        form = "Exit {}:  {: <{}} --> {}"
        return form.format(self.name,
                           self.barrier, barrier_width,
                           self.destination)
    
    def json_encode(self):
        return { "Exit": { "name":          self.name,
                           "destination":   self.destination,
                           "barrier":        self.barrier
                         } }
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Exit" in json_dict:
            name        = json_dict["Exit"]["name"]
            destination = json_dict["Exit"]["destination"]
            barrier     = json_dict["Exit"]["barrier"]
            return Exit(name=name,
                        destination=int(destination),
                        barrier=barrier
                       )
        

class ExitPP(Exit):
    def __init__(self, exit, name_width=0):
        super().__init__(exit.name, exit.destination, exit.barrier)
        self.name_width = name_width

    def __str__(self):
        barrier_width = max([len(b) for b in Exit.cBarriers])
        form = "Exit {: >{}}:  {: <{}} --> {}"
        return form.format(self.name, self.name_width,
                           self.barrier, barrier_width,
                           self.destination) 
     
       
class Board():
    """A collection of interconnected spaces that represent a game board
       with json encode/decode
    """
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
            print("Exception(Board.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Board(json_path)
