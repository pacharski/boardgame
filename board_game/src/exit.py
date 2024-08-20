# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

from copy import deepcopy


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
        return {"__type__":     "Exit",
                "name":         self.name,
                "destination":  self.destination,
                "barrier":      self.barrier
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        exit_dict = (json_dict["Exit"] if "Exit" in json_dict else
                     json_dict if ("__type__" in json_dict) and (json_dict["__type__"] == "Exit") else
                     None)
        if exit_dict != None:
            name        = exit_dict["name"]
            destination = exit_dict["destination"]
            barrier     = exit_dict["barrier"]
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
    
    
if __name__ == "__main__":
    print(ExitPP(Exit()))
    print(ExitPP(Exit("NE Exit", 23, "Secret Door")))
    print(Exit("Dark Tunnel", 12))    