from token import Token

class Player():
    def __init__(self, name, token, cards={}, location=None, id=None):
        self.name = name
        self.id = id
        self.token = token
        self.cards = cards
        self.location = location
        
    def __str__(self):
        form = "Token {}: {} {} at {}"
        return form.format("P" + str(self.id) if self.id != None else "NPC",
                           self.name, self.token, self.location)
    
    def json_encode(self):
        return {"name": self.name,
                "id": self.id,
                "token": self.token.json_encode(),
                "decks": self.cards,
                "location": self.location}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Player" in json_dict:
            name      = json_dict["Player"]["name"]
            id        = json_dict["Player"]["id"]
            token     = json_dict["Player"]["token"]
            decks     = json_dict["Player"]["decks"]
            location  = json_dict["Player"]["location"]
            return Player(name=name,
                          id=id,
                          token=token,
                          decks=decks,
                          location=location
                         )
    
        
if __name__ == '__main__':
    import os
    import json

    class LocalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Player):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Player' in dct:
                return Player.json_decode(dct)
            return dct

    p1   = Player("Fred",    token=Token("", "green"), location=0,    id=1)
    p2   = Player("Daphne",  token=Token("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   token=Token("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  token=Token("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  token=Token("", "white"), location=256,  id=5)
    npc1 = Player("Old Man", token=Token("", "black", "star"), location=12)

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)

    filename = "temp/player.json"
    with open(filename, 'w') as jsonfile:
        json.dump(players, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        players_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(players) == len(players_copy)
    
