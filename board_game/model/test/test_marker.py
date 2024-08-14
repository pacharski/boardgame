import unittest
import json

from model.jsoninator import Jsoninator
from model.marker import Marker

class MarkerTestCase(unittest.TestCase):
    def setUp(self):
        t1 = Marker("G-er", "green", "square") 
        t2 = Marker("B-er", "blue",  "circle") 
        t3 = Marker("R-er", "red",   "triangle")  
        t4 = Marker("R-er", "red",   "triangle")   
        t5 = Marker("W-er", "white", "star")

        self.markers = [t1, t2, t3, t4, t5]

    def test_marker_construct(self):
        t1 = Marker("G-er", "green", "square") 
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
        jsoninator = Jsoninator({"Marker": Marker})
        temp_str = json.dumps(self.markers, default=jsoninator.default)
        markers_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        assert len(self.markers) == len(markers_copy)
        assert self.markers[0].name == markers_copy[0].name
