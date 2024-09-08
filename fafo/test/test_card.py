import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import fafo as ff
import board_game as bg

        
class CardTestCase(unittest.TestCase):
    def setUp(self):
        card1 = ff.Card("Zap",         1,          6)
        card2 = ff.Card("Zop",   value=2, shortcut=7)
        card3 = ff.Card("Phase", value=3, shortcut=8)
        self.cards = [card1, card2, card3]
        self.hand = ff.Deck("Hand", cards=[card1, card1, card3], confidence=3)
        self.draw_pile = ff.Deck("DrawPile", cards=[*(card1 * 3), *(card2 * 4), *(card3 * 5)])
    
    def test_card_construct(self):
        card = ff.Card("Card1", 1, 6)
        self.assertEqual((card.name, card.value, card.shortcut),
                         ("Card1", 1, 6),
                         'Card("Card1", 1, 6) is ("Card1", 1, 6)')
        
    def test_card_mul(self):
        card = ff.Card("Ace", 1, 6)
        cards = card * 4
        self.assertEqual(len(cards), 4, "Card * 4, is list of 4 cards")
        cards[0].name = "King"
        cards[1].value = 2
        for card in cards:
            self.assertEqual((card.name, card.value),
                             ("King", 2),
                             "Cards from mul are shallow copies")
                
    def test_card_json(self):
        jsoninator = bg.Jsoninator({"Card": ff.Card, "Deck": ff.Deck})
        temp_str = json.dumps(self.cards, default=jsoninator.default)
        cards_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
    
        self.assertEqual(len(self.cards),
                         len(cards_copy),
                         "list of cards preserved after json dumps/loads")
        
        for card, card_copy in zip(self.cards, cards_copy):
            self.assertEqual((card.name, card.value, card.shortcut),
                             (card_copy.name, card_copy.value, card_copy.shortcut),
                             "card name/value/shortcut preserved after json dumps/loads")
            

    def test_deck_construct(self):
        deck1 = ff.Deck("Spells", cards=[*(self.cards[0] * 6), *(self.cards[1] * 6), *(self.cards[2] * 4)])
        deck2 = ff.Deck("Test", self.cards, confidence=3)
        self.assertEqual((deck1.name, len(deck1), deck1.confidence),
                         ("Spells", 16, None),
                         "Spells Deck Name/Length match")
        self.assertEqual((deck2.name, len(deck2), deck2.confidence),
                         ("Test", 3, 3),
                         "Test Deck Name/#Cards/#face/#back match")
        
    def test_deck_json(self):
        jsoninator = bg.Jsoninator({"Card": ff.Card, "Deck": ff.Deck})
        temp_str = json.dumps(self.hand, default=jsoninator.default)
        hand_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
    
        self.assertEqual((self.hand.name, len(self.hand), self.hand.confidence),
                         (hand_copy.name, len(hand_copy), 3),
                         "Name/Length of hand preserved after json dumps/loads")
        
        temp_str = json.dumps(self.draw_pile, default=jsoninator.default)
        draw_pile_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
    
        self.assertEqual((self.draw_pile.name, len(self.draw_pile), self.draw_pile.confidence),
                         (draw_pile_copy.name, len(draw_pile_copy), draw_pile_copy.confidence),
                         "Name/Length of draw_pile preserved after json dumps/loads")
        
        for card, card_copy in zip(self.draw_pile, draw_pile_copy):
            self.assertEqual((card.name, card.value),
                             (card_copy.name, card_copy.value),
                             "card name/value preserved after json dumps/loads")
    