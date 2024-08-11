import unittest

import json
import os

from model.json_encoder import CompactJSONEncoder
from model.board import Board
from model.point import Point
from model.space import Space
from model.exit import Exit
        
        
class BoardTestCase(unittest.TestCase):
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

    def test_board_construct(self):
        board = Board()
   
        self.assertEqual((board.spaces, board.last_space_id, board.json_path),
                         (dict(), None, None),
                         "board default is blank")

    def test_board_json(self):
        class LocalEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, (Board, Space, Point, Exit)):
                    return o.json_encode()
                return CompactJSONEncoder.default(self, o)
        
        class LocalDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if "Board" in dct:
                    return Board.json_decode(dct)
                if "Space" in dct:
                    return Space.json_decode(dct)
                if "Point" in dct:
                    return Point.json_decode(dct)
                if "Exit" in dct:
                    return Exit.json_decode(dct)
                return dct

        # here = os.path.abspath(__file__)
        # json_path = os.path.join(os.path.dirname(here), "data/board.json" )
        # print("\n\n", here, "\n\n")

        print("\n\n", os.getcwd(), "\n\n")
        board = Board("../data/board.json")
        self.assertEqual(len(board),
                         419,
                         "saved board load has 419 spaces")

        board.save_to_json_path(json_path="test/temp/board.json")
        board_copy = Board.from_json_path("test/temp/board.json")

        self.assertEqual(len(board_copy),
                         419,
                         "board_copy from json has 419 spaces")
        
        self.assertEqual(board_copy.find_space(Point(100, 100))[0],
                         333,
                         "Space @(100, 100) is 333")
        
        self.assertEqual(board_copy.find_space(Point(200, 100))[0],
                         329,
                         "Space @(200, 100) is 329")
