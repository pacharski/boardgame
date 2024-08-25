from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))
import board_game as bg

class Player(bg.Player):
    def __init__(self, id=None, location=None, name=None, desc=None, marker=None,
                 decks=None, hoard=None):
        super().__init__(id=id, location=location, name=name, desc=desc, marker=marker)
        self.decks = decks if decks != None else dict()
        self.hoard = hoard if hoard != None else bg.Hoard()
        
    def __str__(self):
        form = "{} Decks={} Hoard={}"
        return form.format(super().__str__(),
                           len(self.decks) if self.decks != None else self.decks,
                           self.hoard.value if self.hoard != None else self.hoard)
    
    def json_encode(self):
        return {**super().json_encode(),
                "decks":       self.decks,
                "hoard":       self.hoard
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
            decks     = json_dict["decks"]
            hoard     = json_dict.get("hoard", bg.Hoard())
            return Player(id=id,
                          location=location,
                          name=name,
                          desc=desc,
                          marker=marker,
                          decks=decks,
                          hoard=hoard
                         )
    
        
if __name__ == '__main__':
    card1 = bg.Card("Zap",   "Zap")   
    card2 = bg.Card("Zop",   "Zop")   
    card3 = bg.Card("Phase", "Phase") 

    deck1 = bg.Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9)])
    deck2 = bg.Deck("Spill Cards", cards=[*(card2 * 9), *(card3 * 6)])

    p1   = Player(1,   0, name="Fred",    desc="Driver", marker=bg.Marker("", "green"),
                  decks=None)
    p2   = Player(2,  23, name="Daphne",  desc="Beauty", marker=bg.Marker("", "blue" ))
    p3   = Player(3, 100, name="Velma",   desc="Brains", marker=bg.Marker("", "red"  ))
    p4   = Player(4, 212, name="Scooby",  desc="Knight", marker=bg.Marker("", "red"  ))
    p5   = Player(5, 256, name="Shaggy",  desc="Reason", marker=bg.Marker("", "white"))
    npc1 = Player(location=12, name="Old Man", desc="Sneak", marker=bg.Marker("black", "star"),
                  decks={"deck1": deck1, "deck2": deck2})

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)