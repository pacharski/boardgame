# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import a_game as ag
import board_game as bg


class Game(): 
    def __init__(self, name=None, data_path=None, json_path=None):
        name = name if name != None else "a_game"
        self.data_path = data_path 
        if (data_path == None) and (json_path != None):
            self.data_path = os.path.dirname(json_path)
        self.board_json_path = None if data_path == None else os.path.join(self.data_path, self.name + ".json")
        self.players_json_path = None if data_path == None else os.path.join(self.data_path, "players" + ".json")
        self.hoard_csv_path = None if data_path == None else os.path.join(self.data_path, "hoard" + ".csv")
        self.horde_csv_path = None if data_path == None else os.path.join(self.data_path, "horde" + ".csv")
        self.decks_json_path = None if data_path == None else os.path.join(self.data_path, "decks" + ".json")
        
        if json_path == None:
            self.board = self.create_board()
            self.hoard = self.create_hoard()
            self.horde = self.create_horde()
            self.players = self.create_players()
            self.decks = self.create_decks()
        else:
            self.load_from_json_path(json_path)
            
    def create_board(self):
        return bg.Board() if self.board_json_path == None else bg.Board(json_path=self.board_json_path)
    
    def create_hoard(self):
        return bg.Hoard() if self.hoard_csv_path == None else bg.Hoard(csv_path=self.hoard_csv_path)
     
    def create_horde(self):
        return bg.Horde() if self.horde_csv_path == None else bg.Horde(csv_path=self.horde_csv_path)
    
    def create_players(self):
        if self.players_json_path == None:
            print("NoPlayerPath")
            return list()
        jsoninator = bg.Jsoninator({"Player": ag.Player, "Marker": bg.Marker,
                                    "Deck": bg.Deck, "Card": bg.Card,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature
                                   })
        players_json_path = os.path.join(here, "../../data/players.json" )
        with open(players_json_path, 'r') as json_file:
            return json.load(json_file, object_hook=jsoninator.object_hook)
        
    def create_decks(self):
        # FIXME - read the default decks from data/decks.json (
        if self.decks_json_path == None:
            return dict()
        jsoninator = bg.Jsoninator({"Deck": bg.Deck, "Card": bg.Card,
                                  })
        decks_json_path = os.path.join(here, "../../data/decks.json" )
        with open(decks_json_path, 'r') as json_file:
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
        jsoninator = bg.Jsoninator({"Game": Game,
                                    "Board": ag.Board, "Space": ag.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": bg.Card, "Deck": bg.Deck,
                                    "Player": ag.Player, "Marker": bg.Marker,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature})
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Game": Game,
                                    "Board": ag.Board, "Space": ag.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": bg.Card, "Deck": bg.Deck,
                                    "Player": ag.Player, "Marker": bg.Marker,
                                    "Hoard": bg.Hoard, "Treasure": bg.Treasure,
                                    "Horde": bg.Horde, "Creature": bg.Creature})
        json_path = json_path if json_path != None else self.json_path
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            if isinstance(json_data, dict):
                self.board = json_data["Board"]
                self.players = json_data["Players"]
                self.hoard = json_data["Hoard"]
                self.horde = json_data["Horde"]
                self.decks = json_data["Decks"] if "Decks" in json_data else dict()
            else:
                self.board = json_data.board
                self.players = json_data.players
                self.hoard = json_data.hoard
                self.horde = json_data.horde 
                self.decks = json_data.decks
        except Exception as e:
            print("\nException (Game.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Game(json_path=json_path)


if __name__ == "__main__":
    game = Game()
    #agents = [bg.Agent(player, game.board) for player in game.players]
    print(game)
