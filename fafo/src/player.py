from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

import board_game as bg
import fafo as ff

class Player(bg.Player):
    def __init__(self, id=None, location=None, name=None, desc=None, marker=None, 
                 hand=None):
        super().__init__(id=id, location=location, name=name, desc=desc, marker=marker)
        self.hand = hand if hand != None else bg.Deck("Hand")
        
    def __str__(self):
        form = "{} Hand={}"
        return form.format(super().__str__(), len(self.hand))
                           
    def json_encode(self):
        return {**super().json_encode(),
                "hand": self.hand
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        player_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Player")) else
                       None)
        if player_dict != None:
            id        = json_dict["id"]
            location  = json_dict["location"]
            name      = json_dict["name"]
            desc      = json_dict["desc"]
            marker    = json_dict["marker"]
            hand      = json_dict.get("hand", bg.Deck("Hand"))
            return Player(id=id,
                          location=location,
                          name=name,
                          desc=desc,
                          marker=marker,
                          hand=hand
                         )
    
        
if __name__ == '__main__':
    card1 = ff.Card("Ogre",   2,  5)
    card2 = ff.Card("Troll",  4,  6)
    card3 = ff.Card("Dragon", 7, 13)

    hand = bg.Deck("Hand", cards=[card1, card2, card3])
    
    p1   = Player(1, 0, "Fred",    "Driver", marker=bg.Marker("green" ), hand=hand)
    p2   = Player(2, 0, "Daphne",  "Beauty", marker=bg.Marker("blue"  )) 
    p3   = Player(3, 0, "Velma",   "Brains", marker=bg.Marker("red"   )) 
    p4   = Player(4, 0, "Scooby",  "Knight", marker=bg.Marker("white" )) 
    
    players = [p1, p2, p3, p4]
    for player in players:
        print(player)