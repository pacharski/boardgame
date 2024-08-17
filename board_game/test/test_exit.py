import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class ExitTestCase(unittest.TestCase):
    def setUp(self):
        e1 = bg.Exit()
        e1.name = "exit1"
        e1.destination = 71
        e1.barrier = "Secret Door"
        e2 = bg.Exit(name="NE Exit", destination=23)
        e2.barrier = "Door"
        e3 = bg.Exit(name="Dark Tunnel", barrier = "")
        e3.destination = 34
        e4 = e3.deep_copy()
        e4.destination = 45
        self.exits = [e1, e2, e3, e4]

    def test_exit_construct_default(self):
        e1 = bg.Exit()
        self.assertEqual((e1.name, e1.destination, e1.barrier, e1.open), 
                         ("", None, "", set()),
                         "Exit: default constructor")
        
    def test_exit_construct(self):
        e2 = bg.Exit(name="NE Exit", destination=23, barrier="Door")
        self.assertEqual((e2.name, e2.destination), 
                         ("NE Exit", 23),
                         "Exit: name, destination set in constructor")
        self.assertEqual(e2.barrier,
                         "Door",
                         "Exit: barrier set in constructor")
        
    def test_exit_copy(self):
        e2 = bg.Exit(name="NE Exit", destination=23, barrier="Door")
        e3 = e2
        e2.name="Dark Tunnel"
        e3.barrier="High Cliff"
        self.assertEqual((e2.name, e2.destination, e2.barrier),
                         ("Dark Tunnel", 23, "High Cliff"),
                        "Exit: shallow copy changed by changing original")
        self.assertEqual((e3.name, e3.destination, e3.barrier),
                         ("Dark Tunnel", 23, "High Cliff"),
                        "Exit: shallow copy changed by changing copy")
       
    def test_exit_deep_copy(self):
        e2 = bg.Exit(name="NE Exit", destination=23, barrier="Door")
        e3 = e2.deep_copy()
        e2.name="Dark Tunnel"
        e3.barrier="High Cliff"
        self.assertEqual((e2.name, e2.destination, e2.barrier),
                         ("Dark Tunnel", 23, "Door"),
                        "Exit: deep copy not changed by changing copy")
        self.assertEqual((e3.name, e3.destination, e3.barrier),
                         ("NE Exit", 23, "High Cliff"),
                        "Exit: deep copy not changed by changing copy")
       
    def test_exit_json(self):
        jsoninator = bg.Jsoninator({"Exit": bg.Exit})
        temp_str = json.dumps(self.exits, default=jsoninator.default)
        exits_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.exits), len(exits_copy),
                         "Length of exits match after json dumps/loads")
        for exit, exit_copy in zip(self.exits, exits_copy):
            self.assertEqual((exit.name, exit.destination, exit.barrier, len(exit.open)),
                             (exit_copy.name, exit_copy.destination, exit_copy.barrier, len(exit_copy.open)),
                             "Exit match after json dumps/loads")