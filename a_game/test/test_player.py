import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import a_game as ag
import board_game as bg


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        card1 = bg.Card(  "Zap",   "Zap")   
        card2 = bg.Card(  "Zop",   "Zop")   
        card3 = bg.Card("Phase", "Phase") 
        
        deck1 = bg.Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9)])
        deck2 = bg.Deck("Spill Cards", cards=[*(card2 * 9), *(card3 * 6)])
        
        p1   = ag.Player(1,   0, name="Fred",    desc="Driver", marker=bg.Marker("", "green"))
        p2   = ag.Player(2,  23, name="Daphne",  desc="Bard",   marker=bg.Marker("", "blue" ))
        p3   = ag.Player(3, 100, name="Velma",   desc="Wizard", marker=bg.Marker("", "red"  ))
        p4   = ag.Player(4, 212, name="Scooby",  desc="Knight", marker=bg.Marker("", "red"  ))
        p5   = ag.Player(5, 256, name="Shaggy",  desc="Rogue",  marker=bg.Marker("", "white"))
        npc1 = ag.Player(location=12, name="Old Man", desc="Creep",  
                         marker=bg.Marker("black", "star"), 
                         decks={"deck1": deck1, "deck2": deck2})
        self.players = [p1, p2, p3, p4, p5, npc1]

    def test_player_construct(self):
        p1 = ag.Player(99, 42, name="Waldo", desc="Sneak",
                       marker=bg.Marker("yellow", "circle", name="W")) 
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
        jsoninator = bg.Jsoninator({"Marker": bg.Marker, "Player": ag.Player,
                                    "Card": bg.Card, "Deck": bg.Deck,
                                    "Treasure": bg.Treasure, "Hoard": bg.Hoard})
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