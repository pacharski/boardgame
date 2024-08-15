import unittest
import json

from model.jsoninator import Jsoninator
from model.marker import Marker
from model.player import Player
from model.card import Card, Deck

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        card1 = Card("Zap",   "Zap")   
        card2 = Card("Zop",   "Zop")   
        card3 = Card("Phase", "Phase") 
        
        deck1 = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9)])
        deck2 = Deck("Spill Cards", cards=[*(card2 * 9), *(card3 * 6)])
        
        p1   = Player("Fred",    "Driver", marker=Marker("", "green"), location=0,    id=1)
        p2   = Player("Daphne",  "Bard",   marker=Marker("", "blue" ), location=23,   id=2)
        p3   = Player("Velma",   "Wizard", marker=Marker("", "red"  ), location=100,  id=3)
        p4   = Player("Scooby",  "Knight", marker=Marker("", "red"  ), location=212,  id=4)
        p5   = Player("Shaggy",  "Rogue",  marker=Marker("", "white"), location=256,  id=5)
        npc1 = Player("Old Man", "Creep",  marker=Marker("", "black", "star"), location=12, decks={"deck1": deck1, "deck2": deck2})
        self.players = [p1, p2, p3, p4, p5, npc1]


    def test_player_construct(self):
        p1 = Player("Waldo", "Sneak", marker=Marker("W", "yellow", "circle"), location=42, id=99) 
        self.assertEqual(p1.name, 
                         "Waldo",
                         "Player: name set in constructor")
        self.assertEqual(p1.desc, 
                         "Sneak",
                         "Player: desc set in constructor")
        self.assertEqual((p1.marker.name, p1.marker.color, p1.marker.shape), 
                         ("W", "yellow", "circle"),
                         "Player: marker set in constructor")
        self.assertEqual(p1.location, 
                         42,
                         "Player: location set in constructor")
        self.assertEqual(p1.id, 
                         99,
                         "Player: id set in constructor")

    def test_player_json(self):
        jsoninator = Jsoninator({"Marker": Marker, "Player": Player,
                                 "Card": Card, "Deck": Deck})
        temp_str = json.dumps(self.players, default=jsoninator.default)
        players_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.players), len(players_copy),
                         "Players match after json dumps/loads")
        for player, player_copy in zip(self.players, players_copy):
            self.assertEqual(player.name, player_copy.name,
                             "Player.name match after json dumps/loads")
            self.assertEqual(player.desc, player_copy.desc,
                             "Player.desc match after json dumps/loads")
            self.assertEqual(player.marker.name, player_copy.marker.name,
                             "Player.marker.name match after json dumps/loads")
            self.assertEqual(player.marker.color, player_copy.marker.color,
                             "Player.marker.name match after json dumps/loads")
            self.assertEqual(player.marker.shape, player_copy.marker.shape,
                             "Player.marker.name match after json dumps/loads")
            self.assertEqual(player.location, player_copy.location,
                             "Player.location match after json dumps/loads")
            self.assertEqual(player.id, player_copy.id,
                             "Player.id match after json dumps/loads")
            self.assertEqual(len(player.decks), len(player_copy.decks),
                             "Player.decks size match after json dumps/loads")
            for deck_name in player.decks.keys():
                self.assertTrue(deck_name in player_copy.decks,
                                "Player.decks key match after json dumps/loads")
                for card, card_copy in zip([c for c in player.decks[deck_name]],
                                           [c for c in player_copy.decks[deck_name]]):
                    self.assertEqual((card.name, card.value),
                                     (card_copy.name, card_copy.value),
                                     "Card name/value match after json dumps/loads")