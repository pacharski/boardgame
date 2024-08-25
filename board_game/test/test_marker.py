import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class MarkerTestCase(unittest.TestCase):
    def setUp(self):
        t1 = bg.Marker("green",   "square", name="G-er") 
        t2 = bg.Marker( "blue",   "circle", size=5) 
        t3 = bg.Marker(  "red", "triangle")  
        t4 = bg.Marker(  "red", "triangle")   
        t5 = bg.Marker("white",     "star", name="W-er")

        self.markers = [t1, t2, t3, t4, t5]

    def test_marker_construct(self):
        t1 = bg.Marker("green", "square", name="G-er") 
        self.assertEqual(t1.name, 
                         "G-er",
                         "Marker: name not set in constructor")
        self.assertEqual(t1.color, 
                         "green",
                         "Marker: color not set in constructor")
        self.assertEqual(t1.shape, 
                         "square",
                         "Marker: shape not set in constructor")

    def test_marker_json(self):
        jsoninator = bg.Jsoninator({"Marker": bg.Marker})
        temp_str = json.dumps(self.markers, default=jsoninator.default)
        markers_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.markers), len(markers_copy),
                         "Markers length match after json dumps/loads")
        for marker, marker_copy in zip(self.markers, markers_copy):
            self.assertEqual(marker.name, marker_copy.name,
                             "Marker.name match after json dumps/loads")
            self.assertEqual(marker.color, marker_copy.color,
                             "Marker.color match after json dumps/loads")
            self.assertEqual(marker.shape, marker_copy.shape,
                             "Marker.shape match after json dumps/loads")
            
