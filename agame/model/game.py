# organization is package/module/submodule
import setup

from model.json_encoder import CompactJSONEncoder
from model.board import Board
from model.space import Space
from model.point import Point
from model.path import Path
from model.exit import Exit
from model.player import Player
from model.marker import Marker
from model.card import Card, Deck
from model.hoard import Hoard, Treasure
from model.horde import Horde, Creature


class Game():
    def __init__(self, data_path=None):
        here = os.path.dirname(os.path.abspath(__file__))
        self.data_path = data_path if data_path != None else os.path.join(here, "../../data")
        self.board_json_path = os.path.join(self.data_path, "board.json" )
        
        self.board = self.create_board()
        self.hoard = self.create_hoard()
        self.horde = self.create_horde()
        self.players = self.create_players()

    def create_board(self):
        return Board(self.board_json_path)
    
    def create_hoard(self):
        csv_path = os.path.join(self.data_path, "treasures.csv" )
        return Hoard.from_csv_path(csv_path)
    
    def create_horde(self):
        csv_path = os.path.join(self.data_path, "creatures.csv" )
        return Horde.from_csv_path(csv_path)
    
    def create_players(self):
        p1   = Player("Elf 1",         marker=Marker("", "green"), location=0, id=1)
        p2   = Player("Elf 1",         marker=Marker("", "green"), location=0, id=2)
        p3   = Player("Hero 2",        marker=Marker("", "blue" ), location=0, id=3)
        p4   = Player("Hero 2",        marker=Marker("", "blue" ), location=0, id=4)
        p5   = Player("Super Hero 1",  marker=Marker("", "red"  ), location=0, id=5)
        p6   = Player("Super Hero 2",  marker=Marker("", "red"  ), location=0, id=6)
        p7   = Player("Wizard 1",      marker=Marker("", "white"), location=0, id=7)
        p8   = Player("Wizard 1",      marker=Marker("", "white"), location=0, id=8)
        return {p.name: p for p in [p1, p2, p3, p4, p5, p6, p7, p8]}
        
    def __str__(self):
        form = "Game: Board={} Players={} Creatures={} Treasures={}"
        return form.format(len(self.board), len(self.players), len(self.horde), len(self.hoard))
        
    def json_encode(self):
        return {"Game": {"Board": self.board,
                         "Players": self.players}}
                        #  "Horde": self.horde,
                        #  "Hoard": self.hoard}}
        
    # Note: this is a class function
    def json_decode(json_dict):
        print("Game.json_decode", json_dict.keys())
        if "Game" in json_dict:
            print("Decode.Board", json_dict.keys())
            board   = json_dict["Game"]["Board"]
            print("Decode.Board", board)
            print("Players", json_dict["Game"])
            players = json_dict["Game"]["Players"]    
            # horde   = Horde.json_decode(json_dict["Game"]["horde"])
            # hoard   = Hoard.json_decode(json_dict["Game"]["hoard"])
            print("AssignGame")
            game = Game()
            game.board = board
            game.players = players
            #game.horde = horde
            #game.hoard = hoard
            return game
        
    def save_to_json_path(self, json_path=None):
        class LocalJSONEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, (Game, Board, Space, Point, Path, Exit,
                                  Player, Marker, Deck, Card)):
                                #   Hoard, Treasure,
                                #   Horde, Creature)):  
                    return o.json_encode()
                elif isinstance(o, (Hoard, Treasure, Horde, Creature)):
                    return None
                return CompactJSONEncoder.default(self, o)
        
        json_path = json_path if json_path != None else os.path.join(self.data_path, "game.json")
        with open(json_path, 'w') as json_file:
                  json.dump(self, json_file, indent=2, sort_keys=False,
                            cls=LocalJSONEncoder, ensure_ascii = False)
        
    # this is a class function and constructs a new Board
    def load_from_json_path(json_path, name=None):
        class LocalJSONDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if 'Point' in dct:
                    return Point.json_decode(dct)
                if 'Space' in dct:
                    return Space.json_decode(dct)
                if 'Path' in dct:
                    return Path.json_decode(dct)
                if 'Exit' in dct:
                    return Exit.json_decode(dct)
                if 'Player' in dct:
                    return Player.json_decode(dct)
                if 'Marker' in dct:
                    return Marker.json_decode(dct)
                if 'Deck' in dct:
                    return Deck.json_decode(dct)
                if 'Card' in dct:
                    return Card.json_decode(dct)
                # if 'Hoard' in dct:
                #     print("Decode.Hoard", dct)
                #     return Hoard.json_decode(dct)
                # if 'Treasure' in dct:
                #     print("Decode.Treasure")
                #     return Treasure.json_decode(dct)
                # if 'Horde' in dct:
                #     print("Decode.Horde", dct)
                #     return Horde.json_decode(dct)
                # if 'Creature' in dct:
                #     print("Decode.Creature")
                #     return Creature.json_decode(dct)
                return dct
            
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, cls=LocalJSONDecoder)
            # game is a dictionary of Board, Players, Hoard, Horde
            # players is a list of Player
            # Hoard and Horde are from readonly csv, and not json serializable
            game = Game()
            game.board = Board.json_decode({"Board": json_data["Game"]["Board"]})
            game.players = json_data["Game"]["Players"]
            return game
        except Exception as e:
            # print exception to help with debugging bad json
            print("Exception (Game.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Game(json_path)


if __name__ == "__main__":
    import os
    import json 

    game = Game()
    
    here = os.path.abspath(__file__)
    temp_path = "agame/model/temp/game.json"
    game.save_to_json_path(json_path=temp_path)
    game = Game.load_from_json_path(json_path=temp_path)

    assert game != None
    if game != None:
        print(game)
        assert len(game.board) == 419
        