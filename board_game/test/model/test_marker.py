import unittest
from model.marker import Marker

class MarkerTestCase(unittest.TestCase):
    def setUp(self):
        t1 = Marker("G-er", "green", "square") 
        t2 = Marker("B-er", "blue",  "circle") 
        t3 = Marker("R-er", "red",   "triangle")  
        t4 = Marker("R-er", "red",   "triangle")   
        t5 = Marker("W-er", "white", "star")

        self.markers = [t1, t2, t3, t4, t5]
        for marker in self.markers:
            print(marker)

    def test_create_with_name_color_shape(self):
        t1 = Marker("G-er", "green", "square") 
        print(t1)
        self.assertEqual(t1.name, 
                         "G-er",
                         "Marker: name not set in constructor")
        self.assertEqual(t1.color, 
                         "green",
                         "Marker: color not set in constructor")
        self.assertEqual(t1.shape, 
                         "square",
                         "Marker: shape not set in constructor")

    def test_read_write_json(self):
        import json
        from model.json_encoder import CompactJSONEncoder

        class LocalEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, Marker):
                    return o.json_encode()
                return CompactJSONEncoder.default(self, o)
        
        class LocalDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if "Marker" in dct:
                    return Marker.json_decode(dct)
                return dct

        filename = "temp/marker.json"
        with open(filename, 'w') as jsonfile:
            json.dump(self.markers, jsonfile, cls=LocalEncoder)
        with open(filename, 'r') as jsonfile:
            markers_copy = json.load(jsonfile, cls=LocalDecoder)

        assert len(self.markers) == len(markers_copy)
        assert self.markers[0].name == markers_copy[0].name
