from card import Card, Deck

class Layout():
    """"Define the size and location of components of a card style and value"""
    def __init__(self, name="", blocking=[]):
        self.name = name
        self.blocking = blocking

    def __str__(self):
        form = "Layout: {} blocking={}"
        return form.format(self.name, len(self.blocking))
    
    def __len__(self):
        return len(self.blocking)

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
    def __init__(self, name="", components={}, layout=[]):
        self.name         = name
        self.components   = components
        self.layout       = layout

    def __str__(self):
        form = "Style: {} Components={} Layout={}"
        return form.format(self.name, 
                           len(self.components), len(self.layout)) 
    
    def json_encode(self):
        return {"Style": {"name":          self.name,
                          "components":    self.components,
                          "layout":        self.layout}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "Style" in json_dict:
            name         = json_dict["Style"]["name"]
            components   = json_dict["Style"]["components"]
            layout       = json_dict["Style"]["layout"]
            return Style(name, components=components, layout=layout)
            
    
class CardView():
    """Display a card on tkinter canvas"""
    def __init__(self, card, front=None, back=None):
        self.card = card
        self.front = front
        self.back = back

    def __str__(self):
        form = "CardView: {} Front={} Back={}"
        return form.format(self.card, self.front, self.back)
    
    def json_encode(self):
        return {"CardView": {"card":     self.card,
                             "front":    self.front,
                             "back":     self.back}}
    
    # Note: this is a class function
    def json_decode(json_dict):
        if "CardView" in json_dict:
            card         = json_dict["CardView"]["card"]
            front        = json_dict["CardView"]["front"]
            back         = json_dict["CardView"]["back"]
            return CardView(card, front=front, back=back)
   
    
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
            if isinstance(o, (Style, Layout, CardView, Deck, Card)):
                return o.json_encode()
            return CompactJSONEncoder.default(self, o)
    
    class LocalDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if "Style" in dct:
                return Deck.json_decode(dct)
            if "Layout" in dct:
                return Deck.json_decode(dct)
            if "CardView" in dct:
                return Deck.json_decode(dct)
            if "Deck" in dct:
                return Deck.json_decode(dct)
            if "Card" in dct:
                return Card.json_decode(dct)
            return dct

    front = Style("Spell Front", components={}, layout=Layout("front_layout"))
    back = Style("Spell Back", components={})
    print(front)
    print(back)
    print()
    
    card1 = Card("Zap",   "Zap")
    card2 = Card("Zop",   "Zop")
    card3 = Card("Phase", "Phase")
    print(card1)
    print(card2)
    print(card3)
    print()

    deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    print("Deck", deck)

    card_views = [CardView(card, front=front, back=back) for card in deck]
    for card_view in card_views:
        print(card_view)
    print()

    filename = "temp/style.json"
    styles = {"front": front,
              "back":  back}
    with open(filename, 'w') as jsonfile:
        json.dump(styles, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        styles_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(styles) == len(styles_copy)
    assert "front" in styles_copy
    assert "back" in styles_copy
 
    filename = "temp/card_view.json"
    with open(filename, 'w') as jsonfile:
        json.dump(card_views, jsonfile, cls=LocalEncoder)
    with open(filename, 'r') as jsonfile:
        card_views_copy = json.load(jsonfile, cls=LocalDecoder)

    assert len(card_views) == len(card_views_copy)
    #assert "front" in styles_copy
    #assert "back" in styles_copy
 