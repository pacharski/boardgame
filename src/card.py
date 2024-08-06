class Style():
    def __init__(self, name, 
                 color="white", image_path=None, image=None, 
                 border_width=0, border_color="gold", 
                 text="", text_color="black"):
        self.name         = name
        self.color        = color
        self.image_path   = image_path
        self.image        = image
        self.border_width = border_width
        self.border_color = border_color
        self.text         = text
        self.text_color   = text_color

    def __str__(self):
        form = "Style {}: {}/{}/{}"
        return form.format(self.name, 
                           self.color, self.image_path, self.text) 
    
    def json_encode(self):
        return {"Style": {"name":          self.name,
                          "color":         self.color,
                          "image_path":    self.image_path,
                          "border_width":  self.border_width,
                          "border_color":  self.border_color,
                          "text":          self.text,
                          "text_color":    self.text_color
                         } 
               }
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Style" in json_dict:
            name         = json_dict["Style"]["name"]
            color        = json_dict["Style"]["color"]
            image_path   = json_dict["Style"]["image_path"]
            image        = None
            border_width = json_dict["Style"]["border_width"]
            border_color = json_dict["Style"]["border_color"]
            text         = json_dict["Style"]["text"]
            text_color   = json_dict["Style"]["text_color"]
            return Style(name, color=color, image_path=image_path, image=image,
                        border_width=int(border_width), border_color=border_color,
                        text=text, text_color=text_color)

    
class Card():
    def __init__(self, name, text=None, front=None, back=None):
        self.name = name
        self.text = text
        self.front = front
        self.back = back

    def __mul__(self, n):
        return [self for _ in range(n)]

    def __str__(self):
        form = "Card {}: Text={} Front={} Back={}"
        return form.format(self.name, 
                           (self.text if self.text != None else
                            self.front.text if self.front != None and self.front.text != None else
                            ""),
                           self.front, self.back)
                           
    def json_encode(self):
        return {"Card": {"name": self.name,
                         "text": self.text,
                         "front": self.front.json_encode() if self.front != None else self.front,
                         "back": self.back.json_encode() if self.back != None else self.back}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Card" in json_dict:
            name      = json_dict["Card"]["name"]
            text      = json_dict["Card"]["text"]
            front     = json_dict["Card"]["front"]
            back      = json_dict["Card"]["back"]
            return Card(name, text=text, front=front, back=back)
    
    
class Deck():
    def __init__(self, name, cards=[]):
        self.name = name
        self.cards = cards

    def __iter__(self):
        for card in self.cards:
            yield card

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        form = "Deck {}: {} cards"
        return (form.format(self.name, len(self.cards)) if isinstance(self.cards, list) else
                "Invalid")
    
    def json_encode(self):
        return {"Deck": {"name":  self.name,
                         "cards": self.cards}}
                
    # Note: this is a class function
    def json_decode(json_dict):
        if "Deck" in json_dict:
            name      = json_dict["Deck"]["name"]
            #cards     = [Card.json_decode(card_dict) for card_dict in json_dict["cards"]]
            cards     = json_dict["Deck"]["cards"]
            return Deck(name=name, cards=cards)

        
if __name__ == '__main__':
    import os
    import json
    from json_encoder import CompactJSONEncoder

    class LocalEncoder(CompactJSONEncoder):
        def default(self, o):
            if isinstance(o, (Deck, Card, Style)):
                return o.json_encode()
            return CompactJSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if "Deck" in dct:
                return Deck.json_decode(dct)
            if "Card" in dct:
                return Card.json_decode(dct)
            if "Style" in dct:
                return Style.json_decode(dct)
            return dct
    
    front = Style("Spell Front", color="white", text_color="black")
    back = Style("Spell Back", color="black", text_color="white", text="Spell")
    print(front)
    print(back)
    print()
    
    card1 = Card("Zap",   text="Zap",   front=front, back=back)
    card2 = Card("Zop",   text="Zop",   front=front, back=back)
    card3 = Card("Phase", text="Phase", front=front, back=back)
    print(card1)
    print(card2)
    print(card3)
    print()

    # Shallow copy of cards is okay because they are immutable
    # FIXME - store front/back styles for the deck, but allow override of front by card
    deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    print("Deck", deck)
    for card in deck:
        print(card)
    print()

    filename = "temp/style.json"
    with open(filename, 'w') as jsonfile:
        json.dump(front, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        front_copy = json.load(jsonfile, cls=LocalDecoder)

    print(type(front), type(front_copy))
    assert(front.name == front_copy.name)
    assert(front.color == front_copy.color)
    assert(front.image_path == front_copy.image_path)
    assert(front.border_width == front_copy.border_width)
    assert(front.border_color == front_copy.border_color)
    assert(front.text == front_copy.text)

    filename = "temp/card.json"
    with open(filename, 'w') as jsonfile:
        json.dump(card1, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        card1_copy = json.load(jsonfile, cls=LocalDecoder)

    print(type(card1), type(card1_copy))
    assert(card1.name == card1_copy.name)
    assert(card1.text == card1_copy.text)
    assert(card1.front.name == card1_copy.front.name)
    assert(card1.back.name == card1_copy.back.name)
    
    filename = "temp/deck.json"
    with open(filename, 'w') as jsonfile:
        json.dump(deck, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        deck_copy = json.load(jsonfile, cls=LocalDecoder)

    print("Started", len(deck), "Finished", len(deck_copy))
    assert(len(deck) == len(deck_copy))