class Layout():
    """"Define the size and location of components of a card style and value"""
    def __init__(self, name, blocking={}):
        self.name = name
        self.properties = blocking

    def __str__(self):
        form = "Layout: {} blocking={}"
        return form.format(self.name, self.blocking.keys())

    def json_encode(self):
        return {"Layout": {"name":       self.name,
                           "blocking":   self.blocking}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Layout" in json_dict:
            name         = json_dict["Layout"]["name"]
            blocking     = json_dict["Layout"]["blocking"]
            return Layout(name, blocking=blocking)
            

class Style():
    """Define the colors and layout of a card face or back"""
    def __init__(self, name, components={}, blocking={})
        self.name         = name
        self.components   = components
        self.blocking     = blocking

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

    
class CardView():
    """Display a card on tkinter canvas"""
    def __init__(self, card, front=None, back=None):
        self.card = card
        self.front = front
        self.back = back

    def __str__(self):
        form = "CardView: {} Front={} Back={}"
        return form.format(self.card, self.front, self.back)
    
    
class DeckView():
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

        
if __name__ == '__main__':
    import os
    import json
    from json_encoder import CompactJSONEncoder

    class LocalEncoder(CompactJSONEncoder):
        def default(self, o):
            if isinstance(o, (Deck, Card)):
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

    deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    print("Deck", deck)
    for card in deck:
        print(card)
    print()

    