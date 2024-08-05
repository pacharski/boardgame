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
        

if __name__ == '__main__':
    p1   = Player("Fred",    token=Token("", "green"), location=0,    id=1)
    p2   = Player("Daphne",  token=Token("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   token=Token("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  token=Token("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  token=Token("", "white"), location=256,  id=5)
    npc1 = Player("Old Man", token=Token("", "black", "star"), location=12)

    players = [p1, p2, p3, p4, p5, npc1]
    for player in players:
        print(player)
