import unittest

import json

from board_game.model.jsoninator import Jsoninator
from board_game.model.point import Point

        
class PointTestCase(unittest.TestCase):
    def setUp(self):
        p1 = Point()
        p2 = Point(x=5)
        p3 = Point(y=4)
        p4 = Point(x=6, y=8)
        p5 = p4.deep_copy()
        p5.y = 12
        self.points = [p1, p2, p3, p4, p5]

    def test_point_default(self):
        point = Point()
        self.assertEqual((point.x, point.y),
                         (0, 0),
                         "point default is (0, 0)")
        
    def test_point_x_only(self):
        point = Point(x=5)
        self.assertEqual((point.x, point.y),
                            (5, 0),
                            "Point(x=5) is (5, 0)")
        
    def test_point_y_only(self):
        point = Point(y=7)
        self.assertEqual((point.x, point.y),
                            (0, 7),
                            "Point(y=7) is (0, 7)")
    
    def test_point_deep_copy(self):
        point = Point(x=5, y=7)
        point_copy = point
        point.x=6
        point_deep_copy = point.deep_copy()
        point_deep_copy.x=10
        point_deep_copy.y=11
        self.assertEqual((point.x, point.y),
                            (6, 7),
                            "point changed to (6, 7)")
        self.assertEqual((point_copy.x, point_copy.y),
                            (6, 7),
                            "point_copy was changed becauase point was changed")
        self.assertEqual(point_deep_copy.xy,
                            (10, 11),
                            "point_deep_copy was not changed when point was changed")
        
    def test_point_equal(self):
        point1 = Point(5, 6)
        point1_copy = point1
        point2 = Point(5, 6)
        point3 = Point(5, 8)
        point4 = Point(7, 6)
        point5 = Point()
        self.assertNotEqual(point1, None, "point not equal None")
        self.assertEqual(point1, point1_copy, "point equal shallow_copy of self")
        self.assertEqual(point1, point2, "point equal point with same xy")
        self.assertNotEqual(point1, point3, "point not equal if different y")
        self.assertNotEqual(point1, point4, "point not equal if different x")
        self.assertNotEqual(point1, point5, "point not equal if different x and y")
            
    def test_point_json(self):
        jsoninator = Jsoninator({"Point": Point})
        temp_str = json.dumps(self.points, default=jsoninator.default) 
        points_copy = json.loads(temp_str, object_hook=jsoninator.object_hook) 
    
        self.assertEqual(len(self.points),
                             len(points_copy),
                             "list of points preserved after json file write/read")
        
        for point, point_copy in zip(self.points, points_copy):
            self.assertEqual(point.xy,
                             point_copy.xy,
                             "point xy preserved after json file write/read")
            