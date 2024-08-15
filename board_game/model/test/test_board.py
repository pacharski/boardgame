import unittest 

import json
import os

import setup
from model.jsoninator import Jsoninator
from model.board import Board
from model.point import Point
from model.space import Space
from model.exit import Exit
from model.path import Path


class BoardTestCase(unittest.TestCase):
    def setUp(self):
        here = os.path.abspath(__file__)
        self.json_path = os.path.join(os.path.dirname(here), "../../../data/board.json" )
        
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
        board = Board(self.json_path)
        self.assertEqual(len(board), 419,
                         "saved board load has 419 spaces")
        
        jsoninator = Jsoninator({"Board": Board, "Space": Space, 
                                "Point": Point, "Path": Path, "Exit": Exit})
        temp_str = json.dumps(board, default=jsoninator.default)
        board_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(board_copy), 419,
                         "board_copy from json has 419 spaces")
        
        self.assertEqual(board_copy.find_space(Point(100, 100))[0],
                         333,
                         "Space @(100, 100) is 333")
        
        self.assertEqual(board_copy.find_space(Point(200, 100))[0],
                         329,
                         "Space @(200, 100) is 329")
        
        board.save_to_json_path("board.json")
        board_copy = Board.from_json_path("board.json")
    
        self.assertEqual(len(board_copy), 419,
                         "board_copy from json(file) has 419 spaces")
        
        self.assertEqual(board_copy.find_space(Point(100, 100))[0],
                         333,
                         "Space(file) @(100, 100) is 333")
        
        self.assertEqual(board_copy.find_space(Point(200, 100))[0],
                         329,
                         "Space(file) @(200, 100) is 329")
