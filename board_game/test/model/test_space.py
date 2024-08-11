import unittest

import json

from model.space import Space
from model.point import Point
from model.json_encoder import CompactJSONEncoder
        
        
class SpaceTestCase(unittest.TestCase):
    def setUp(self):
        s1 = Space()
        s2 = Space(id=2, name="Crypt", center=Point(5, 6), level=4)
        s3 = Space(id=3, name="Queen's Crypt", center=Point(5, 6), level=4)
        s3.vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)]
        s4 = Space(name="Queen's Crypt", center=Point(5, 6), level=4,
                vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)])
        s4.add_vertex(Point(7,8))
        s5 = s4.deep_copy()
        s5.add_vertex(Point(11,12))
        self.spaces = [s1, s2, s3, s4, s5]

    def test_read_write_json(self):
        class LocalEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Space):
                    return o.json_encode()
                return json.JSONEncoder.default(self, o)
            
        class LocalDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if 'Space' in dct:
                    return Space.json_decode(dct)
                return dct

        json_path = "temp/space.json"
        with open(json_path, 'w') as json_file:
            json.dump(self.spaces, json_file, cls=LocalEncoder)
        with open(json_path, 'r') as json_file:
            self.spaces_copy = json.load(json_file, cls=LocalDecoder)
        
        def test_create_with_name_color_shape(self):
            self.assertEqual(len(spaces),
                             len(spaces_copy),
                             "Len(spaces) not the same after json write/read")
            for idx in range(len(spaces)):
                self.assertEqual(spaces[idx].id,
                                 spaces_copy[idx].id,
                                 "space id not the same after json write/read")
                self.assertEqual(spaces[idx].name,
                                 spaces_copy[idx].name,
                                 "space name not the same after json write/read")
                self.assertEqual(spaces[idx].level,
                                 spaces_copy[idx].level,
                                 "space level not the same after json write/read")
                self.assertEqual(spaces[idx].center,
                                 spaces_copy[idx].center,
                                 "space center not the same after json write/read")
                self.assertEqual(len(spaces[idx].vertices),
                                 len(spaces_copy[idx].vertices),
                                 "space vertices count not the same after json write/read")
                self.assertEqual(len(spaces[idx].exits),
                                 len(spaces_copy[idx].exits),
                                 "space exits count not the same after json write/read")
