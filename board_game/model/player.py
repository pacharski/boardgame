# organization is package/module/submodule
import setup

from marker import Marker

class Player():
    def __init__(self, name, marker, decks={}, location=None, id=None):
        self.name = name
        self.id = id
        self.marker = marker
        self.decks = decks
        self.location = location
        
    def __str__(self):
        form = "Player {}: {} Marker={} Decks={} at {}"
        return form.format("P" + str(self.id) if self.id != None else "NPC",
                           self.name, self.marker, len(self.decks), self.location)
    
    def json_encode(self):
        return {"Player": {"name": self.name,
                           "id": self.id,
                           "marker": self.marker.json_encode(),
                           "decks": self.decks,
                           "location": self.location}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Player" in json_dict:
            name      = json_dict["Player"]["name"]
            id        = json_dict["Player"]["id"]
            marker    = json_dict["Player"]["marker"]
            decks     = json_dict["Player"]["decks"]
            location  = json_dict["Player"]["location"]
            return Player(name=name,
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

    p1   = Player("Fred",    marker=Marker("", "green"), location=0,    id=1)
    p2   = Player("Daphne",  marker=Marker("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   marker=Marker("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  marker=Marker("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  marker=Marker("", "white"), location=256,  id=5)
    npc1 = Player("Old Man", marker=Marker("", "black", "star"), location=12, decks={"deck1": deck1, "deck2": deck2})

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)