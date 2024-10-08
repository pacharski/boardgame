from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import random


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
    """A collection (list) of Cards"""
    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards if cards != None else []
        
    def add(self, cards):
        if isinstance(cards, (list, tuple)):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)

    def draw(self, remove=True):
        if remove:
            return self.cards.pop() if len(self.cards) > 0 else None
        return self.cards[0]
    
    def remove(self, card):
        self.cards.remove(card)

    def remove_all(self):
        self.cards = []
        
    def shuffle(self):
        if self.cards != None:
            random.shuffle(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def __getitem__(self, index):
        return self.cards[index]
    
    def __setitem__(self, index, value):
        self.cards[index] = value

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        form = "Deck: {} size={}"
        size = len(self.cards) if isinstance(self.cards, list) else "Invalid"
        return form.format(self.name, size)
        
    def json_encode(self):
        print("BoardGame.Deck.Encode")
        return {"__type__": "Deck",
                "name":     self.name,
                "cards":    self.cards
               }
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Deck")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            cards     = local_dict["cards"]
            return Deck(name=name, cards=cards)
        return json_dict
    

class DecoratedDeck(Deck):
    """A collection (list) of Cards with common components of the face and back"""
    def __init__(self, name, cards=None, face=None, back=None):
        super().__init__(name=name, cards=cards)
        self.face = face
        self.back = back

    def json_encode(self):
        return {"__type__": "DecoratedDeck",
                "name":     self.name,
                "cards":    self.cards,
                "face":     self.face,
                "back":     self.back
               }
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "DecoratedDeck")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            cards     = local_dict["cards"]
            face      = local_dict["face"]
            back      = local_dict["back"]
            return DecoratedDeck(name=name, cards=cards, face=face, back=back)
        return json_dict