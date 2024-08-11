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

    def test_space_construct(self):
        space = Space()
        self.assertTrue(isinstance(space, Space), "Space() constructs object of type Space")
        self.assertEqual((space.id, space.name, space.level, space.center, 
                          len(space.vertices), len(space.exits)),
                         (-1, "space", -1, None, 0, 0),
                         "space default is blank")
        
    def test_space_center_is_type_Point(self):
        space = Space(id=2, name="Crypt", center=Point(5, 6), level=4)
        self.assertTrue(isinstance(space .center, Point), "space.center is type Point")

    def test_space_json(self):
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

        json_path = "test/temp/space.json"
        with open(json_path, 'w') as json_file:
            json.dump(self.spaces, json_file, cls=LocalEncoder)
        with open(json_path, 'r') as json_file:
            spaces_copy = json.load(json_file, cls=LocalDecoder)

        self.assertEqual(len(self.spaces),
                            len(spaces_copy),
                            "Len(spaces) not the same after json write/read")
        
        for space, space_copy in zip(self.spaces, spaces_copy):
            self.assertTrue(isinstance(space, Space), "space for json write is type Space")
            self.assertTrue(isinstance(space_copy, Space), "space from json read is type Space")
            self.assertEqual(space.id,
                             space_copy.id,
                             "space id not the same after json write/read")
            self.assertEqual(space.name,
                             space_copy.name,
                             "space name not the same after json write/read")
            self.assertEqual(space.level,
                             space_copy.level,
                             "space level not the same after json write/read")
            self.assertEqual(space.center,
                             space_copy.center,
                             "space center not the same after json write/read")
            self.assertEqual(len(space.vertices),
                             len(space_copy.vertices),
                             "space vertices count not the same after json write/read")
            self.assertEqual(len(space.exits),
                             len(space_copy.exits),
                             "space exits count not the same after json write/read")
