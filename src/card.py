class Card():
    def __init__(self, name, 
                 front_color="white", front_image=None, front_outline_color="gold", 
                 front_text="", front_text_color="black",
                 back_color="black", back_image=None, back_outline_color="gold", 
                 back_text="", back_text_color="white"
                ):
        self.name = name
        self.front_color = front_color
        self.front_image = front_image
        self.front_outline_color = front_outline_color
        self.front_text = front_text
        self.front_text_color = front_text_color
        self.back_color = back_color
        self.back_image = back_image
        self.back_outline_color = back_outline_color
        self.back_text = back_text
        self.back_text_color = back_text_color

    def __mul__(self, n):
        return [self for _ in range(n)]

   
    def __str__(self):
        form = "Card {}: {}/{}/{} {}/{}/{}"
        return form.format(self.name, 
                           self.front_color, self.front_image, self.front_text,
                           self.back_color, self.back_image, self.back_text) 
    
class Deck():
    def __init__(self, name, cards=[]):
        self.name = name
        self.cards = cards

    def __iter__(self):
        for card in self.cards:
            yield card

    def __str__(self):
        form = "Deck {}: {} cards"
        return (form.format(self.name, len(self.cards)) if isinstance(self.cards, list) else
                "Invalid")

        
if __name__ == '__main__':
    card1 = Card("Zap",   front_text="Zap",   back_text="Spell")
    card2 = Card("Zop",   front_text="Zop",   back_text="Spell")
    card3 = Card("Phase", front_text="Phase", back_text="Spell")
    # Shallow copy of cards is okay because they are immutable
    deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    print("Deck", deck)
        
    for card in deck:
        print(card)