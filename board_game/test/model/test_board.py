import unittest

from model.board import Board
from model.point import Point
from model.space import Space
from model.exit import Exit

class BoardTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_write_json(self):
        import os
        import json
        from model.json_encoder import CompactJSONEncoder

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

        here = os.path.abspath(__file__)
        print("Here", here)
        json_path = os.path.join(os.path.dirname(here), "../../../data/board.json" )
        print("JsonPath", json_path)

        board = Board(json_path)
        assert len(board) == 419
        board.save_to_json_path(json_path="temp/board.json")
        board1 = Board("temp/board.json")
        board2 = Board.from_json_path("temp/board.json")

        print(board1)
        assert len(board1.spaces) == len(board2.spaces)
        assert len(board1.spaces) == 419
        assert len(board1) == 419
    
        print("Find(100,100)", board1.find_space(Point(100, 100)))
        assert board1.find_space(Point(100, 100))[0] == 333
        print("Find(200,100)", board1.find_space(Point(200, 100)))
        assert board1.find_space(Point(200, 100))[0] == 329
        
