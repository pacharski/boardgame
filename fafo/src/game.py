import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))

import json
import csv
import random
import fafo as ff
import board_game as bg


class GameAction():
    def __init__(self, action, card=None, location=None, other_player=None):
        self.action = action
        self.card = card
        self.location = location
        self.other_player = other_player
        
    def __str__(self):
        if self.action == "Move":
            form = "move to {there}"
            return form.format(there=self.location)
        elif self.action == "Challenge":
            form = "challenge {other_player} at {there} with {card}"
            return form.format(other_player=self.other_player.name, 
                               there=self.other_player.location,
                               card=self.card.name)
        else:
            form = "Action: {action}"
            return form.format(action=self.action)
        

class GameState():
    def __init__(self, players, heros, winner):
        self.players = players
        self.heros = heros
        self.winner = winner

    def state_for_player(self, player):
        # Player knows own hand, but not others
        pass


class Game(): 
    def __init__(self, name=None, data_path=None, json_path=None):
        self.name = name if name != None else "fafo"
        self.data_path = data_path 
        if (data_path == None) and (json_path != None):
            self.data_path = os.path.dirname(json_path)
        self.board_json_path = None if data_path == None else os.path.join(self.data_path, self.name + ".json")
        self.players_json_path = None if data_path == None else os.path.join(self.data_path, "players" + ".json")
        self.cards_csv_path = None if data_path == None else os.path.join(self.data_path, "cards" + ".csv")
        self.winner = None

        if json_path == None:
            self.board = self.create_board()
            self.players = self.create_players()
            self.draw_pile, self.discard_pile = self.create_cards()
            random.shuffle(self.draw_pile)
        else:
            self.load_from_json_path(json_path)

    def create_board(self):
        return ff.Board() if self.board_json_path == None else ff.Board(json_path=self.board_json_path)
    
    def create_players(self):
        if self.players_json_path == None:
            return list()
        jsoninator = bg.Jsoninator({"Player": ff.Player, "Marker": bg.Marker,
                                    "Deck": ff.Deck, "Card": ff.Card,
                                  })
        with open(self.players_json_path, 'r') as json_file:
            return json.load(json_file, object_hook=jsoninator.object_hook)
        
    def create_cards(self):
        draw = ff.Deck("Draw")
        discard = ff.Deck("Discard")
        if self.cards_csv_path != None:
            with open(self.cards_csv_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if len(row) != 4:
                        # print("SkipCard(#)", len(row), row)
                        count = 0
                    else:
                        count, level, shortcut, desc = row
                        try:
                            count = int(count)
                            card = ff.Card(desc.strip(), int(level), int(shortcut))
                            draw.add(card * count)
                        except Exception as e:
                            # print("SkipCard(value)", len(row), row)
                            # print(e)
                            count = 0
        return draw, discard
    
    def restock(self):
        self.draw_pile = self.discard_pile
        self.draw_pile.name = "Draw"
        self.draw_pile.shuffle()
        self.discard_pile = ff.Deck("Discard")
    
    def draw(self, name="someone"):
        if len(self.draw_pile) == 0:
            self.restock()
        card = self.draw_pile.draw() if len(self.draw_pile) > 0 else None
        return card

    def discard(self, card, name="someone"):
        self.discard_pile.add(card)  
        return card  
    
    def exit_available(self, exit, space, shortcuts=None):
        if exit.barrier == "Shortcut":
            if shortcuts == None:
                return False
            for shortcut in shortcuts:
                if shortcut in [name.strip() for name in space.name.split(',')]:
                    return True
            return False
        return True
                
    def forward_exits_for_location(self, location):
        forwards = [exit for exit in self.board.spaces[location].exits
                    if exit.barrier == "Forward"]
        return forwards    
                    
    def backward_exits_for_location(self, location):
        backwards = [exit for exit in self.board.spaces[location]
                     if exit.barrier == "Backward"]
        return backwards  

    def space_at_location(self, location: int):
        return self.board.spaces[location] if location != None else None  
    
    def move_choices(self, space: bg.Space, moves_left: int,
                     shortcuts=[], exit_types=("Forward", "Shortcut"), final=False):
        """ Return a list of possible move action lists starting at space and
             using the number of moves list by taking available exit_types """
        moves = [] 
        if moves_left == 0:
            if not final:
              moves = moves + [[ff.GameAction(None, None, "SpaceAction")]]
        else: 
            exits = [e for e in space.exits 
                     if ((e.barrier in exit_types)
                     and self.exit_available(e, space, shortcuts=shortcuts))]
            for exit in exits:
                if exit.barrier == "":
                    print("NoBarrier", exit_types)
                elif len(exit.barrier) == 0:
                    print("ZeroBarrier")
                exit_action = ff.GameAction("Move", location=exit.destination)
                next_choices = self.move_choices(
                    self.space_at_location(exit.destination),
                    moves_left-1, shortcuts, exit_types, final)
                 # at the end, next_choices will be an empty list
                if len(next_choices) > 0:
                    for move_choice in next_choices:
                        extended = [exit_action]
                        extended.extend(move_choice)
                        moves.append(extended)
                else:
                    moves.append([exit_action])
        return moves
    
    def challenge_choices(self, player: bg.Player, card: bg.Card):
        other_players = [other_player for other_player in self.players 
                         if ((other_player != player) 
                         and (other_player.location != None))]
        # challenge_choices = []
        # for other_player in other_players:
        #     challenge_choices.append([ff.GameAction("Challenge",
        #                                             card=card,
        #                                             location=player.location,
        #                                             other_player=player)])
        return [ff.GameAction("Challenge", card=card,
                              location=player.location, other_player=other_player)
                for other_player in other_players]
    
    def game_state(self):
        return GameState(self.players, [])
                    
    def __str__(self):
        form = "Fafo: Board={} Players={} Cards={}"
        return form.format(len(self.board), len(self.players), len(self.draw_pile))
        
    def json_encode(self):
        return {"__type__":     "Game",
                "Board":        self.board,
                "Players":      self.players,
                "DrawPile":     self.draw_pile,
                "DiscardPile":  self.discard_pile}
        
    # Note: this is a class function
    def json_decode(json_dict):
        game_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Game")) else
                     None)
        if game_dict != None:
            board        = game_dict["Board"]
            players      = game_dict["Players"]    
            draw_pile    = game_dict["DrawPile"]
            discard_pile = game_dict["DiscardPile"]
            game = Game()
            game.board = board
            game.players = players
            game.draw_pile = draw_pile
            game.discard_pile = discard_pile
            return game
        return json_dict
    
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Game": Game,
                                    "Board": ff.Board, "Space": ff.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": ff.Card, "Deck": ff.Deck,
                                    "Player": ff.Player, "Marker": bg.Marker
                                  })
        json_path = json_path if json_path != None else self.json_path
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
            
    # this is a class function and constructs a new Board
    def load_from_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Game": Game,
                                    "Board": ff.Board, "Space": ff.Space, "Point": bg.Point,
                                    "Exit": bg.Exit, "Connection": bg.Connection,
                                    "Card": ff.Card, "Deck": ff.Deck,
                                    "Player": ff.Player, "Marker": bg.Marker
                                  })
        json_path = json_path if json_path != None else self.json_path
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            self.board = json_data.board
            self.players = json_data.players
            self.draw_pile = json_data.draw_pile
            self.discard_pile = json_data.discard_pile
        except Exception as e:
            print("\nException (Game.load_from_json_path)", e)
            pass

    def from_json_path(json_path):
        return Game(json_path=json_path)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print("Here", here)
    game = Game("fafo", os.path.join(os.path.dirname(here), "data"))
    #agents = [bg.Agent(player, game.board) for player in game.players]
    print(game)
