import unittest

import json

import setup
from model.jsoninator import Jsoninator
from model.space import Space
from model.point import Point
        
        
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
        jsoninator = Jsoninator({"Point": Point, "Space": Space})
        temp_str = json.dumps(self.spaces, default=jsoninator.default)
        spaces_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

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
