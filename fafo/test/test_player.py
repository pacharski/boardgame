import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import fafo as ff
import board_game as bg


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        card1 = ff.Card(  "Zap", 1, 5)
        card2 = ff.Card(  "Zop", 2, 6)
        card3 = ff.Card("Phase", 3, 7)
        
        hand1 = bg.Deck("Hand", cards=[card1, card2, card3])
        hand2 = bg.Deck("Hand", cards=[card1, card1, card2])
        hand3 = bg.Deck("Hand", cards=[card2, card2, card2])
        hand4 = bg.Deck("Hand", cards=[card3, card3, card3])
        
        p1   = ff.Player(1,   0, name="Fred",    desc="Driver", 
                         marker=bg.Marker("green"), hand=hand1)
        p2   = ff.Player(2,  23, name="Daphne",  desc="Bard",   
                         marker=bg.Marker("blue" ), hand=hand2)
        p3   = ff.Player(3, 100, name="Velma",   desc="Wizard", 
                         marker=bg.Marker("red"  ), hand=hand3)
        p4   = ff.Player(4, 101, name="Scooby",  desc="Knight", 
                         marker=bg.Marker("white"), hand=hand4)
        self.players = [p1, p2, p3, p4]

    def test_player_construct(self):
        p1 = ff.Player(99, 42, name="Waldo", desc="Sneak",
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
        jsoninator = bg.Jsoninator({"Marker": bg.Marker, "Player": ff.Player,
                                    "Card": ff.Card, "Deck": bg.Deck})
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
            self.assertEqual(len(player.hand), len(player_copy.hand),
                             "Player.hand size match after json dumps/loads")
            for card, card_copy in zip([c for c in player.hand],
                                       [c for c in player_copy.hand]):
                self.assertEqual((card.name, card.value, card.shortcut),
                                 (card_copy.name, card_copy.value, card_copy.shortcut),
                                 "Card name/value/shortcut match after json dumps/loads")