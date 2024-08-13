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
        return {"__type__": "Card",
                "name":     self.name,
                "value":    self.value}
    
    # Note: this is a class function
    def json_decode(json_dict):
        local_dict = (json_dict["Card"] if "Card" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Card")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            value     = local_dict["value"]
            return Card(name, value=value)
        return json_dict
    
    
class Deck():
    """A collection (list) of Cards with common components of the face and back"""
    def __init__(self, name, cards=[], face=None, back=None):
        self.name = name
        self.cards = cards
        self.face = face
        self.back = back

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
        return {"__type__": "Deck",
                "name":     self.name,
                "cards":    self.cards,
                "face":     self.face,
                "back":     self.back}
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict["Deck"] if "Deck" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Deck")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            cards     = local_dict["cards"]
            face      = local_dict["face"]
            back      = local_dict["back"]
            return Deck(name=name, cards=cards, face=face, back=back)
        return Card.json_decode(json_dict)

        
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