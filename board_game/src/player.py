# organization is project/package/module/submodule

from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))
import board_game as bg

class Player():
    def __init__(self, id=None, location=None, name=None, desc=None, marker=None):
        self.id = id
        self.location = location
        self.name = name
        self.desc = desc
        self.marker = marker
        
    def __str__(self):
        form = "Player: {id} at {location} {name} {desc} Marker={color}-{shape}"
        return form.format(id=("P" + str(self.id) if self.id != None else "NPC"),
                           location=(self.location if self.location != None else "Nowhere"), 
                           name=(self.name if self.name != None else "Nobody"), 
                           desc=(self.desc if self.desc != None else "Non-descript"),
                           color=(self.marker.color if self.marker != None else None),
                           shape=(self.marker.shape if self.marker != None else None))
                           
    def json_encode(self):
        return {"__type__":    "Player",
                "id":          self.id,
                "location":    self.location,
                "name":        self.name,
                "desc":        self.desc,
                "marker":      self.marker, #.json_encode(),
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        #player_dict = (json_dict["Player"] if ("Player" in json_dict) else
        player_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Player")) else
                       None)
        if player_dict != None:
            id        = json_dict["id"]
            location  = json_dict["location"]
            name      = json_dict["name"]
            desc      = json_dict["desc"]
            marker    = json_dict["marker"]
            return Player(id=id,
                          location=location,
                          name=name,
                          desc=desc,
                          marker=marker
                         )
    
        
if __name__ == '__main__':
    p1   = Player(id=1, location=1, name="Fred",    desc="Driver", marker=bg.Marker("", "green"))
    p2   = Player(id=1, location=1, name="Daphne",  desc="Beauty", marker=bg.Marker("", "blue" ))
    p3   = Player(id=1, location=1, name="Velma",   desc="Brains", marker=bg.Marker("", "red"  ))
    p4   = Player(id=1, location=1, name="Scooby",  desc="Knight", marker=bg.Marker("", "red"  ))
    p5   = Player(id=1, location=1, name="Shaggy",  desc="Reason", marker=bg.Marker("", "white"))
    npc1 = Player(id=1, location=1, name="Old Man", desc="Sneak",  marker=bg.Marker("", "black", "star"))

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)