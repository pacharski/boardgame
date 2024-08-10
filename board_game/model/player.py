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
    import os
    import json
    from json_encoder import CompactJSONEncoder
    from card import Card, Deck

    class LocalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (Card, Deck, Marker, Player)):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if "Card" in dct:
                return Card.json_decode(dct)
            if "Deck" in dct:
                return Deck.json_decode(dct)
            if "Marker" in dct:
                return Marker.json_decode(dct)
            if "Player" in dct:
                return Player.json_decode(dct)
            return dct
        
    card1 = Card("Zap",   "Zap")   
    card2 = Card("Zop",   "Zop")   
    card3 = Card("Phase", "Phase") 
    print(card1)
    print(card2)
    print(card3)
    print()

    deck1 = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9)])
    deck2 = Deck("Spill Cards", cards=[*(card2 * 9), *(card3 * 6)])
    print("Deck1", deck1)
    for card in deck1:
        print(card)
    print()

    p1   = Player("Fred",    marker=Marker("", "green"), location=0,    id=1)
    p2   = Player("Daphne",  marker=Marker("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   marker=Marker("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  marker=Marker("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  marker=Marker("", "white"), location=256,  id=5)
    npc1 = Player("Old Man", marker=Marker("", "black", "star"), location=12, decks={"deck1": deck1, "deck2": deck2})

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)

    filename = "temp/player.json"
    with open(filename, 'w') as jsonfile:
        json.dump(players, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        players_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(players) == len(players_copy)
    assert players[5].name == "Old Man"
    npc_copy = players[5]
    assert "deck1" in npc_copy.decks
    assert "deck2" in npc_copy.decks
    assert npc_copy.decks["deck1"].name == "Spell Cards"
    assert npc_copy.decks["deck2"].name == "Spill Cards"
    
