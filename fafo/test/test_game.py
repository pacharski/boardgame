import unittest 

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import a_game as ag
import board_game as bg


class GameTestCase(unittest.TestCase):
    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(here, "../../data" )
        board_json_path = os.path.join(here, "../../data/board.json" )
        self.board = bg.Board(board_json_path)

        jsoninator = bg.Jsoninator({"Player": bg.Player, "Marker": bg.Marker,
                                    "Deck": bg.Deck, "Card": bg.Card,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature
                                   })
        players_json_path = os.path.join(here, "../../data/players.json" )
        with open(players_json_path, 'r') as json_file:
            self.players = json.load(json_file, object_hook=jsoninator.object_hook)
        
        hoard_json_path = os.path.join(here, "../../data/hoard.json" )
        self.hoard = bg.Hoard(json_path=hoard_json_path)
        horde_json_path = os.path.join(here, "../../data/horde.json" )
        self.horde = bg.Horde(json_path=horde_json_path)
        

    def test_game_construct_default(self):
        game = ag.Game()
        self.assertEqual((len(game.board), len(game.players), len(game.hoard), len(game.horde)),
                         (0, 0, 0, 0),
                         "Default game has no spaces, players, treasures or creatures")

    def test_game_json_str(self):
        game = ag.Game()
        game.board = self.board
        game.players = self.players
        game.hoard = self.hoard
        game.horde = self.horde
        
        jsoninator = bg.Jsoninator({"Game": ag.Game, "Board": bg.Board,
                                    "Point": bg.Point, "Space": bg.Space,
                                    "Exit": bg.Exit, "Connection": bg.Connection, 
                                    "Player": bg.Player, "Marker": bg.Marker,
                                    "Deck": bg.Deck, "Card": bg.Card,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature
                                   })
        temp_str = json.dumps(game, default=jsoninator.default)
        game_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
        
        self.assertEqual(len(game.board), 419, "Test Game length is 419") 
        self.assertEqual(len(game.board), len(game_copy.board), 
                         "Game board length match after json dumps/loads")
        self.assertEqual(len(game.players), 8, "Test Players length is 8")
        self.assertEqual(len(game.players), len(game_copy.players), 
                         "Game players length match after json dumps/loads")
        self.assertEqual(len(game.hoard), 80, "Test Hoard length is 80")
        self.assertEqual(len(game.hoard), len(game_copy.hoard), 
                         "Game hoard length match after json dumps/loads")
        self.assertEqual(len(game.horde), 61, "Test Hoard length is 61")
        self.assertEqual(len(game.horde), len(game_copy.horde), 
                         "Game horde length match after json dumps/loads")
        
    def test_game_json_file(self):
        game = ag.Game()
        game.board = self.board
        game.players = self.players
        game.hoard = self.hoard
        game.horde = self.horde
        
        jsoninator = bg.Jsoninator({"Game": ag.Game, "Board": bg.Board,
                                    "Point": bg.Point, "Space": bg.Space,
                                    "Exit": bg.Exit, "Connection": bg.Connection, 
                                    "Player": bg.Player, "Marker": bg.Marker,
                                    "Deck": bg.Deck, "Card": bg.Card,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature
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
        self.assertEqual(len(game.hoard), 80, "Test Hoard length is 80")
        self.assertEqual(len(game.hoard), len(game_copy.hoard), 
                         "Game hoard length match after json dumps/loads")
        self.assertEqual(len(game.horde), 61, "Test Hoard length is 61")
        self.assertEqual(len(game.horde), len(game_copy.horde), 
                         "Game horde length match after json dumps/loads")
        
            