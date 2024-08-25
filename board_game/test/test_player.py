import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        p0   = bg.Player(id=0, location=1, name="Mystery Van", desc="Vehicle", marker=bg.Marker("", "green"))
        p1   = bg.Player(1,    1,   "Fred",  "Driver", bg.Marker("green"))
        p2   = bg.Player(2,    1, "Daphne",    "Bard", bg.Marker("blue" ))
        p3   = bg.Player(3,    1,  "Velma",  "Wizard", bg.Marker("red"  ))
        p4   = bg.Player(4,  256, "Scooby",  "Knight", bg.Marker("red"  ))
        p5   = bg.Player(5, None, "Shaggy",   "Rogue", bg.Marker("white"))
        npc1 = bg.Player(name="Old Man", desc="Creep", marker=bg.Marker("black", "star"),
                         location=12)
        self.players = [p0, p1, p2, p3, p4, p5, npc1]


    def test_player_construct(self):
        p1 = bg.Player(99, name="Waldo", desc="Sneak", marker=bg.Marker("yellow", "circle", name="W"), 
                       location=42) 
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
        jsoninator = bg.Jsoninator({"Marker": bg.Marker, "Player": bg.Player,
                                    "Card": bg.Card, "Deck": bg.Deck})
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
            