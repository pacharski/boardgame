# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import board_game as bg


class Game(): 
    def __init__(self, name=None, data_path=None):
        name = name if name != None else ""
        self.data_path = data_path
        # if data_path == None:
        #     here = os.path.dirname(os.path.abspath(__file__))
        #     self.data_path = data_path if data_path != None else os.path.join(here, "../../data")
        self.board_json_path = None if data_path == None else os.path.join(self.data_path, "board" + ".json")
        self.players_json_path = None if data_path == None else os.path.join(self.data_path, "players" + ".json")
        self.hoard_csv_path = None if data_path == None else os.path.join(self.data_path, "hoard" + ".csv")
        self.hoard_json_path = None if data_path == None else os.path.join(self.data_path, "hoard" + ".json")
        self.horde_csv_path = None if data_path == None else os.path.join(self.data_path, "horde" + ".csv")
        self.horde_json_path = None if data_path == None else os.path.join(self.data_path, "horde" + ".json")
        
        self.board = self.create_board()
        self.hoard = self.create_hoard()
        self.horde = self.create_horde()
        self.players = self.create_players()

    def create_board(self):
        return bg.Board() if self.board_json_path == None else bg.Board(json_path=self.board_json_path)
    
    def create_hoard(self):
        return bg.Hoard() if self.hoard_csv_path == None else bg.Hoard(csv_path=self.hoard_csv_path)
     
    def create_horde(self):
        return bg.Horde() if self.horde_csv_path == None else bg.Horde(csv_path=self.horde_csv_path)
    
    def create_players(self):
        # FIXME - read the default players from data/players.json (need jsoninator for list of players)
        if self.players_json_path == None:
            return list()
        jsoninator = bg.Jsoninator({"Player": bg.Player, "Marker": bg.Marker,
                                    "Deck": bg.Deck, "Card": bg.Card,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature
                                   })
        players_json_path = os.path.join(here, "../../data/players.json" )
        with open(players_json_path, 'r') as json_file:
            return json.load(json_file, object_hook=jsoninator.object_hook)
        
    def __str__(self):
        form = "Game: Board={} Players={} Creatures={} Treasures={}"
        return form.format(len(self.board), len(self.players), len(self.horde), len(self.hoard))
        
    def json_encode(self):
        return {"__type__": "Game",
                "Board":    self.board,
                "Players":  self.players,
                "Horde":    self.horde,
                "Hoard":    self.hoard}
        
    # Note: this is a class function
    def json_decode(json_dict):
        game_dict = (json_dict["Game"] if ("Game" in json_dict) else
                     json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Game")) else
                     None)
        if game_dict != None:
            board   = game_dict["Board"]
            players = game_dict["Players"]    
            horde   = game_dict["Horde"]
            hoard   = game_dict["Hoard"]
            game = Game()
            game.board = board
            game.players = players
            game.horde = horde
            game.hoard = hoard
            return game
        return json_dict
    
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": bg.Board, "Space": bg.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": bg.Card, "Deck": bg.Deck,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Board": bg.Board, "Space": bg.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": bg.Card, "Deck": bg.Deck,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature})
        json_path = json_path if json_path != None else self.json_path
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            if isinstance(json_data, dict):
                game = Game()
                game.board = json_data["Board"]
                game.players = json_data["Players"]
                game.hoard = json_data["Hoard"]
                game.horde = json_data["Horde"]
                return game
            else:
                self.board = json_data.board
                self.players = json_data.players
                self.hoard = json_data.hoard
                self.horde = json_data.horde 
        except Exception as e:
            print("\nException (Game.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Game(json_path)


if __name__ == "__main__":
    game = Game()
    print(game)
