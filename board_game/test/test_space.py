import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg
        
        
class SpaceTestCase(unittest.TestCase):
    def setUp(self):
        s1 = bg.Space()
        s2 = bg.Space(id=2, name="Crypt", center=bg.Point(5, 6), level=4)
        s3 = bg.Space(id=3, name="Queen's Crypt", center=bg.Point(5, 6), level=4)
        s3.vertices = [bg.Point(0, 0), bg.Point(0, 5), bg.Point(4, 5), bg.Point(4, 0)]
        s4 = bg.Space(name="Queen's Crypt", center=bg.Point(5, 6), level=4,
                      vertices = [bg.Point(0, 0), bg.Point(0, 5), bg.Point(4, 5), bg.Point(4, 0)])
        s4.add_vertex(bg.Point(7,8))
        s5 = s4.deep_copy()
        s5.add_vertex(bg.Point(11,12))
        self.spaces = [s1, s2, s3, s4, s5]

    def test_space_construct(self):
        space = bg.Space()
        self.assertTrue(isinstance(space, bg.Space), "Space() constructs object of type Space")
        self.assertEqual((space.id, space.name, space.level, space.center, 
                          len(space.vertices), len(space.exits)),
                         (-1, "space", -1, None, 0, 0),
                         "space default is blank")
        
    def test_space_center_is_type_Point(self):
        space = bg.Space(id=2, name="Crypt", center=bg.Point(5, 6), level=4)
        self.assertTrue(isinstance(space .center, bg.Point), "space.center is type Point")

    def test_space_json(self):
        jsoninator = bg.Jsoninator({"Point": bg.Point, "Space": bg.Space})
        temp_str = json.dumps(self.spaces, default=jsoninator.default)
        spaces_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.spaces),
                         len(spaces_copy),
                         "Len(spaces) not the same after json write/read")
        
        for space, space_copy in zip(self.spaces, spaces_copy):
            self.assertTrue(isinstance(space, bg.Space), "space for json write is type Space")
            self.assertTrue(isinstance(space_copy, bg.Space), "space from json read is type Space")
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
