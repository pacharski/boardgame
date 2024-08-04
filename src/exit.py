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
        open = set(self.open)
        return Exit(self.name, self.destination, self.barrier, open=open)

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
    
    
import json 
if __name__ == "__main__":
    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Exit):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
        
    class Decoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Exit' in dct:
                return Exit.json_decode(dct)
            return dct

    e1 = Exit()
    e1.name = "exit1"
    e1.destination = 71
    e1.barrier = "Secret Door"
    
    e2 = Exit(name="NE Exit", destination=23)
    e2.barrier = "Door"

    e3 = Exit(name="Dark Tunnel", barrier = "")
    e3.destination = 34

    e4 = e3.deep_copy()

    exits = [e1, e2, e3, e4]
    
    name_width = max([len(e.name) for e in exits]) + 2
    print(ExitPP(e1, name_width))
    print(ExitPP(e2, name_width))
    print(ExitPP(e3, name_width))
    print(ExitPP(e4, name_width))
    print()
 
    filename = "temp/exit.json"
    with open(filename, 'w') as jsonfile:
        json.dump(exits, jsonfile, cls=Encoder)
    with open(filename, 'r') as jsonfile:
        exits_copy = json.load(jsonfile, cls=Decoder)
    assert len(exits) == len(exits_copy)
    name_width = max([len(e.name) for e in exits])
    for idx in range(len(exits)):
        exit = exits[idx]
        exit_copy = exits_copy[idx]
        print("{} == {}".format(ExitPP(exit, name_width), ExitPP(exit_copy, name_width)))
        assert exit.name        == exit_copy.name
        assert exit.destination == exit_copy.destination
        assert exit.barrier      == exit_copy.barrier
        