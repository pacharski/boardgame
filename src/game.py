from json_encoder import CompactJSONEncoder
from board import Board
from space import Space
from point import Point
from path import Path
from exit import Exit
from player import Player
from token import Token
from card import Card, Deck


class Game():
    def __init__(self, name=None, board=None, players={},
                 npcs={}, decks={}):
        self.name = name if name != None else ""
        self.board = board
        self.players = players
        self.npcs = npcs
        self.decks = decks

    def __str__(self):
        form = "Game: {} Players={} Npcs={} Decks={}"
        return form.format(self.name, len(self.players), len(self.npcs), len(self.decks))
        
    def json_encode(self):
        return {"name": self.name,
                "board": board.json_encode(),
                "players": self.players,
                "npcs": self.npcs,
                "decks": self.decks}
        
    # Note: this is a class function
    def json_decode(json_dict):
        # if "Game" in json_dict:
        #     name   = json_dict["Game"]["name"]
        #     board  = json_dict["Game"]["board"]    
        #     spaces = json_dict["Game"]["players"]
        #     npcs   = json_dict["Game"]["npcs"]
        #     decks  = json_dict["Game"]["decks"]
        #     return Game(name=name,
        #                 board=board,
        #                 players=players,
        #                 npcs=npcs,
        #                 decks=decks
        #                )
        pass
        
    def save_to_json_file(self, json_path=None):
        class LocalJSONEncoder(CompactJSONEncoder):
            def default(self, o):
                if isinstance(o, (Game, Board, Space, Point, Path, Exit, Player, Token, Deck, Card)):  
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
                    return Exit.json_decode(dct)
                if 'Token' in dct:
                    return Exit.json_decode(dct)
                if 'Deck' in dct:
                    return Exit.json_decode(dct)
                if 'Card' in dct:
                    return Exit.json_decode(dct)
                return dct
            
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, cls=LocalJSONDecoder)
            game = Game()
            game.name = json_data.get("name", "") if name == None else name
            game.board = json_data.get("board", None)
            game.players = json_data.get("players", {})
            game.npcs = json_data.get("npcs", {})
            game.decks = json_data.get("decks", {})
            return game
        except Exception as e:
            # print exception to help with debugging bad json
            print("Exception", e)
            pass


if __name__ == "__main__":
    import os
    import json 

    name = "A Game"
    
    here = os.path.abspath(__file__)
    json_path = os.path.join(os.path.dirname(here), "../data/board.json" )
    board = Board.load_from_json_file(json_path, name="GameBoard")

    p1   = Player("Fred",    token=Token("", "green"), location=0,    id=1)
    p2   = Player("Daphne",  token=Token("", "blue" ), location=23,   id=2)
    p3   = Player("Velma",   token=Token("", "red"  ), location=100,  id=3)
    p4   = Player("Scooby",  token=Token("", "red"  ), location=212,  id=4)
    p5   = Player("Shaggy",  token=Token("", "white"), location=256,  id=5)
    players = {p.name: p for p in [p1, p2, p3, p4, p5]}

    npc1 = Player("Old Man",  token=Token("", "black", "star"), location=12)
    npc2 = Player("Henchman", token=Token("", "bluw", "star"),  location=13)
    npcs = {p.name: p for p in [npc1, npc2]}
        
    card1 = Card("Zap",   front_text="Zap",   back_text="Spell")
    card2 = Card("Zop",   front_text="Zop",   back_text="Spell")
    card3 = Card("Phase", front_text="Phase", back_text="Spell")
    deck1 = Deck("Spell Cards", cards=[*(card1 * 9), *(card2 * 9), *(card3 * 6)])
    
    treasure_cards = [Card(str(value)+"gp" for value in range(100, 2500, 100))]
    deck2 = Deck("Treasure Cards", cards=treasure_cards)
    decks = {d.name: d for d in [deck1, deck2]}
    
    game = Game("A Game", board=board, players=players, npcs=npcs, decks=decks)
    print("Game", game)

    game.save_to_json_file(json_path="temp/game.json")
    game = Game.load_from_json_file(json_path="temp/game.json")

    assert(game != None)
    if game != None:
        print("Game", game.name, game.board)
        assert(game.name == "A Game")
    