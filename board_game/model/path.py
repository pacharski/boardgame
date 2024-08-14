# organization is package/module/submodule
import setup

from enum import IntEnum


class Path():
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
                       forward=Type.cClear, backward=None):
        self.name      = name
        self.origin    = origin
        self.terminus  = terminus
        self.forward   = forward
        self.backward  = backward if backward != None else self.forward

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