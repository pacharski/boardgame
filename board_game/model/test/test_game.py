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
    def __init__(self):
        self.board = self.create_board()
        self.hoard = self.create_hoard()
        self.horde = self.create_horde()
        self.players = self.create_players()

    def create_board(self):
        here = os.path.abspath(__file__)
        json_path = os.path.join(os.path.dirname(here), "../data/board.json" )
        return Board.load_from_json_file(json_path)
    
    def create_hoard(self):
        here = os.path.abspath(__file__)
        csv_path = os.path.join(os.path.dirname(here), "../data/treasures.csv" )
        return Hoard.from_csv_file(csv_path)
    
    def create_horde(self):
        here = os.path.abspath(__file__)
        csv_path = os.path.join(os.path.dirname(here), "../data/creatures.csv" )
        return Horde.from_csv_file(csv_path)
    
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
        form = "Game: Players={} Creatures={} Treasures={}"
        return form.format(len(self.players), len(self.horde), len(self.hoard))
        
    def json_encode(self):
        return {"Game": {"board": self.board,
                         "players": self.players,
                         "horde": self.horde,
                         "hoard": self.hoard}}
        
    # Note: this is a class function
    def json_decode(json_dict):
        if "Game" in json_dict:
            board   = Board.json_decode(json_dict["Dungeon"]["board"])
            players = json_dict["Dungeon"]["players"]    
            horde   = Horde.json_decode(json_dict["Dungeon"]["horde"])
            hoard   = Hoard.json_decode(json_dict["Dungeon"]["hoard"])
            game = Game()
            game.board = board
            game.players = players
            game.horde = horde
            game.hoard = hoard
            return game
        
    def save_to_json_file(self, json_path=None):
        class LocalJSONEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, (Game, Board, Space, Point, Path, Exit, 
                                  Player, Marker, Deck, Card,
                                  Hoard, Treasure,
                                  Horde, Creature)):  
                    return o.json_encode()
                return CompactJSONEncoder.default(self, o)
        
        json_path = json_path if json_path != None else self.json_path
        print("SaveToFile", json_path)
        
        with open(json_path, 'w') as json_file:
                  json.dump(self, json_file, indent=2, sort_keys=False,
                            cls=LocalJSONEncoder, ensure_ascii = False)
            
    # this is a class function and constructs a new Board
    def load_from_json_file(json_path, name=None):
        class LocalJSONDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
            def object_hook(self, dct):
                if 'Game' in dct:
                    return Game.json_decode(dct)
                if 'Board' in dct:
                    return Board.json_decode(dct)
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
                if 'Hoard' in dct:
                    return Hoard.json_decode(dct)
                if 'Treasure' in dct:
                    return Treasure.json_decode(dct)
                if 'Horde' in dct:
                    return Horde.json_decode(dct)
                if 'Creature' in dct:
                    return Creature.json_decode(dct)
                return dct
            
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, cls=LocalJSONDecoder)
            game = json_data["Game"]
            return game
        except Exception as e:
            # print exception to help with debugging bad json
            print("Exception", e)
            pass


if __name__ == "__main__":
    import os
    import json 

    game = Game()
    
    here = os.path.abspath(__file__)
    game.save_to_json_file(json_path="temp/game.json")
    game = Game.load_from_json_file(json_path="temp/game.json")

    assert game != None
    if game != None:
        print(game)
        assert len(game.board) == 419
        