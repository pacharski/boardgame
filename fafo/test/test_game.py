import unittest 

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import fafo as ff
import board_game as bg


class GameTestCase(unittest.TestCase):
    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(here, "../../data" )
        board_json_path = os.path.join(here, "../../data/board.json" )
        self.board = ff.Board(board_json_path)

        jsoninator = bg.Jsoninator({"Player": ff.Player, "Marker": bg.Marker,
                                    "Deck": ff.Deck, "Card": ff.Card,
                                    })
        players_json_path = os.path.join(here, "../../data/players.json" )
        with open(players_json_path, 'r') as json_file:
            self.players = json.load(json_file, object_hook=jsoninator.object_hook)
        
        hoard_json_path = os.path.join(here, "../../data/hoard.json" )
        self.hoard = bg.Hoard(json_path=hoard_json_path)
        horde_json_path = os.path.join(here, "../../data/horde.json" )
        self.horde = bg.Horde(json_path=horde_json_path)
        

    def test_game_construct_default(self):
        game = ff.Game()
        self.assertEqual((len(game.board), len(game.players)),
                         (0, 0),
                         "Default game has no spaces, players")

    def test_game_json_str(self):
        game = ff.Game()
        game.board = self.board
        game.players = self.players
        
        jsoninator = bg.Jsoninator({"Game": ff.Game, "Board": ff.Board,
                                    "Point": bg.Point, "Space": ff.Space,
                                    "Exit": bg.Exit, "Connection": bg.Connection, 
                                    "Player": ff.Player, "Marker": bg.Marker,
                                    "Deck": ff.Deck, "Card": ff.Card,
                                    })
        temp_str = json.dumps(game, default=jsoninator.default)
        game_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
        
        self.assertEqual(len(game.board), 419, "Test Game length is 419") 
        self.assertEqual(len(game.board), len(game_copy.board), 
                         "Game board length match after json dumps/loads")
        self.assertEqual(len(game.players), 8, "Test Players length is 8")
        self.assertEqual(len(game.players), len(game_copy.players), 
                         "Game players length match after json dumps/loads")
        
    def test_game_json_file(self):
        game = ff.Game()
        game.board = self.board
        game.players = self.players
        
        jsoninator = bg.Jsoninator({"Game": ff.Game, "Board": ff.Board,
                                    "Point": bg.Point, "Space": ff.Space,
                                    "Exit": bg.Exit, "Connection": bg.Connection, 
                                    "Player": ff.Player, "Marker": bg.Marker,
                                    "Deck": ff.Deck, "Card": ff.Card,
                                    })
        game_json_path = os.path.join(here, "../../data/game.json" )
        with open(game_json_path, 'w') as json_file:
            json.dump(game, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
        with open(game_json_path, 'r') as json_file:
                game_copy = json.load(json_file, object_hook=jsoninator.object_hook)
            
        self.assertEqual(len(game.board), 419, "Test Game length is 419") 
        self.assertEqual(len(game.board), len(game_copy.board), 
                         "Game board length match after json dumps/loads")
        self.assertEqual(len(game.players), 8, "Test Players length is 8")
        self.assertEqual(len(game.players), len(game_copy.players), 
                         "Game players length match after json dumps/loads")
        
            