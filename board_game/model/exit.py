# organization is package/module/submodule
import setup

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
    
    
if __name__ == "__main__":
    print(ExitPP(Exit()))
    print(ExitPP(Exit("NE Exit", 23, "Secret Door")))
    print(Exit("Dark Tunnel", 12))    