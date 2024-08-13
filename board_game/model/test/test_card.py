import unittest

import json

from model.json_encoder import CompactJSONEncoder
from board_game.model.card import Card, Deck

        
class CardTestCase(unittest.TestCase):
    def setUp(self):
        card1 = Card("Zap",   value="Zap")
        card2 = Card("Zop",   value="Zop")
        card3 = Card("Phase", value="Phase")
        self.cards = [card1, card2, card3]
        self.deck = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    
    def test_card_construct(self):
        card = Card("Card1", "Value1")
        self.assertEqual((card.name, card.value),
                         ("Card1", "Value1"),
                         'Card("Card1", "Value1") is ("Card1", "Value1")')
        
    def test_card_mul(self):
        card = Card("Ace", "Hearts")
        cards = card * 4
        self.assertEqual(len(cards), 4, "Card * 4, is list of 4 cards")
        cards[0].name = "King"
        cards[1].value = "Clubs"
        for card in cards:
            self.assertEqual((card.name, card.value),
                             ("King", "Clubs"),
                             "Cards from mul are shallow copies")
                
    def test_card_json(self):
        class LocalEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Card):
                    return o.json_encode()
                return json.JSONEncoder.default(self, o)

        temp_str = json.dumps(self.cards, cls=LocalEncoder)
        cards_copy = json.loads(temp_str, object_hook=Card.json_decode)
    
        self.assertEqual(len(self.cards),
                             len(cards_copy),
                             "list of cards preserved after json dumps/loads")
        
        for card, card_copy in zip(self.cards, cards_copy):
            self.assertEqual((card.name, card.value),
                             (card_copy.name, card_copy.value),
                             "card name/value preserved after json dumps/loads")
            
    def test_deck_construct(self):
        deck1 = Deck("Spells", cards=[*(self.cards[0] * 6), *(self.cards[1] * 6), *(self.cards[2] * 4)])
        deck2 = Deck("Test", self.cards, 
                     face={"Layout": "Standard", "bg_color": "white", "fg_color": "black"},
                     back={"Image": "CardBack.png", "bg_color": "black", "fg_color": "white", 
                           "text": "Test"})
        self.assertEqual((deck1.name, len(deck1)),
                         ("Spells", 16),
                         "Spells Deck Name/Length match")
        self.assertEqual((deck2.name, len(deck2), len(deck2.face), len(deck2.back)),
                         ("Test", 3, 3, 4),
                         "Test Deck Name/#Cards/#face/#back match")
        
    def test_deck_json(self):
        class LocalEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, (Card, Deck)):
                    return o.json_encode()
                return json.JSONEncoder.default(self, o)

        temp_str = json.dumps(self.deck, cls=LocalEncoder)
        deck_copy = json.loads(temp_str, object_hook=Deck.json_decode)
    
        self.assertEqual((self.deck.name, len(self.deck)),
                         (deck_copy.name, len(deck_copy)),
                         "Name/Length of deck preserved after json dumps/loads")
        
        deck2 = Deck("Deck2", self.cards, 
                     face={"Style": "common"},
                     back={"Layout": "centered", "bg_color": "black"})
        
        temp_str = json.dumps(deck2, cls=LocalEncoder)
        deck2_copy = json.loads(temp_str, object_hook=Deck.json_decode)
    
        self.assertEqual((deck2.name, len(deck2)),
                         (deck2_copy.name, len(deck2_copy)),
                         "Name/Length of deck2 preserved after json dumps/loads")
        
        self.assertEqual((len(deck2.face), deck2.face["Style"]),
                         (1, "common"),
                         "Deck2 face preserved after json dumps/loads")

        self.assertEqual((len(deck2.back), deck2.back["Layout"], deck2.back["bg_color"]),
                         (2, "centered", "black"),
                         "Deck2 back preserved after json dumps/loads")
        
        for card, card_copy in zip(deck2, deck2_copy):
            self.assertEqual((card.name, card.value),
                             (card_copy.name, card_copy.value),
                             "card name/value preserved after json dumps/loads")
    