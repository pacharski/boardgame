# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

from enum import IntEnum


class Connection():
    class Type(IntEnum):
        cClear      = 0
        cDoor       = 1
        cSecretDoor = 2
        cImpasse    = 3

    def type_name(int_type):
        return ("Blocked"     if int_type == Connection.Type.cImpasse else
                "Door"        if int_type == Connection.Type.cDoor else
                "Secret Door" if int_type == Connection.Type.cSecretDoor else
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
        self.forward = Connection.Type.cClear 
        self.backward = Connection.Type.cClear

    def __str__(self):
        types = ["-", "D", "S", "|"]
        form = "Connection: {name}  {origin} <{backward}--{forward}> {terminus}"
        return form.format(name=self.name, origin=self.origin, terminus=self.terminus,
                           forward=types[self.forward], backward=types[self.backward]
                          )
    
    def json_encode(self):
        return {"__type__":   "Connection",
                "name":     self.name,
                "origin":   self.origin,
                "terminus": self.terminus,
                "forward":  self.forward,
                "backward": self.backward
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        if (("Connection" in json_dict)
         or (("__type__" in json_dict) and (json_dict["__type__"] == "Connection"))):   
            name      = json_dict["name"]
            origin    = json_dict["origin"]
            terminus  = json_dict["terminus"]
            forward   = json_dict["forward"]
            backward  = json_dict["backward"]
            return Connection(name=name,
                              origin=int(origin),
                              terminus=int(terminus),
                              forward=int(forward),
                              backward=int(backward)
                             )
        
    
if __name__ == "__main__":
    print(Connection())