# organization is project/package/module/submodule

from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

try:
    from model.marker import Marker
except:
    pass
try:
    from board_game.model import Marker
except:
    pass

class Player():
    def __init__(self, name=None, desc=None, marker=None, decks=None, 
                 location=None, id=None):
        self.name = name
        self.desc = desc
        self.id = id
        self.marker = marker
        self.decks = decks if decks != None else dict()
        self.location = location
        
    def __str__(self):
        form = "Player: {} {} {} {} Decks={} at {}"
        return form.format("P" + str(self.id) if self.id != None else "NPC",
                           self.name, self.desc, self.marker, len(self.decks), self.location)
    
    def json_encode(self):
        return {"__type__":    "Player",
                "name":        self.name,
                "desc":        self.desc,
                "id":          self.id,
                "marker":      self.marker.json_encode(),
                "decks":       self.decks,
                "location":    self.location
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        player_dict = (json_dict["Player"] if ("Player" in json_dict) else
                       json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Player")) else
                       None)
        if player_dict != None:
            name      = json_dict["name"]
            desc      = json_dict["desc"]
            id        = json_dict["id"]
            marker    = json_dict["marker"]
            decks     = json_dict["decks"]
            location  = json_dict["location"]
            return Player(name=name,
                          desc=desc,
                          id=id,
                          marker=marker,
                          decks=decks,
                          location=location
                         )
    
        
if __name__ == '__main__':
    from card import Card, Deck
    card1 = Card("Zap",   "Zap")   
    card2 = Card("Zop",   "Zop")   
    card3 = Card("Phase", "Phase") 

    deck1 = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9)])
    deck2 = Deck("Spill Cards", cards=[*(card2 * 9), *(card3 * 6)])

    p1   = Player("Fred",    "Driver", marker=Marker("", "green"), decks=None, location=0, id=1)
    p2   = Player("Daphne",  "Beauty", marker=Marker("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   "Brains", marker=Marker("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  "Knight", marker=Marker("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  "Reason", marker=Marker("", "white"), location=256,  id=5)
    npc1 = Player("Old Man", "Sneak",  marker=Marker("", "black", "star"), location=12, decks={"deck1": deck1, "deck2": deck2})

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)