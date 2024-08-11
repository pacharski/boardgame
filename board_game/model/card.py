# organization is package/module/submodule
import setup

class Card():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __mul__(self, n):
        return [self for _ in range(n)]

    def __str__(self):
        form = "Card: {} Value={}"
        return form.format(self.name, self.value) 
                           
    def json_encode(self):
        return {"Card": {"name": self.name,
                         "value": self.value}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Card" in json_dict:
            name      = json_dict["Card"]["name"]
            value     = json_dict["Card"]["value"]
            return Card(name, value=value)
    
    
class Deck():
    """A collection (list) of Cards with common components of the face and back"""
    def __init__(self, name, cards=[], face=None, back=None):
        self.name = name
        self.cards = cards

    def __iter__(self):
        for card in self.cards:
            yield card

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        form = "Deck: {} size={}"
        size = len(self.cards) if isinstance(self.cards, list) else "Invalid"
        return form.format(self.name, size)
        
    def json_encode(self):
        return {"Deck": {"name":  self.name,
                         "cards": self.cards}}
                
    # Note: this is a class function
    def json_decode(json_dict):
        if "Deck" in json_dict:
            name      = json_dict["Deck"]["name"]
            cards     = json_dict["Deck"]["cards"]
            return Deck(name=name, cards=cards)

        
if __name__ == '__main__':
    card1 = Card("Zap",   value="Zap")
    card2 = Card("Zop",   value="Zop")
    card3 = Card("Phase", value="Phase")
    print(card1)
    print(card2)
    print(card3)
    print()

    deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    print("Deck", deck)
    print()