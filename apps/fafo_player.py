from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(here))

import tkinter
import random
import fafo as ff
import board_game as bg


class GamePlayer(ff.GameView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.game = ff.Game(self.name, self.data_path)

        # disable all but 4 players
        for pid in range(4, len(self.game.players)):
            self.game.players[pid].location = None
        self.agents = [ff.Agent(player, self.game) 
                       for player in self.game.players if player.location != None]
        self.active_agent = -1
        self.active_actions = []

        self.initial_draw()
        
        self.root = tkinter.Tk()
        self.root.title("Fafo Player")
        frame = tkinter.Frame(self.root)
        frame.pack( fill=tkinter.BOTH, expand=tkinter.YES )
        super().__init__(frame, self.game, self.image_path, (400, 300),
                         bg="white", highlightthickness=0 ) 
        self.focus_set() 

    def bind_mouse(self):
        super().bind_mouse()

    def bind_keys(self):
        super().bind_keys()

    def bind_meta(self):
        super().bind_meta()  

    def apply_overlay(self, bbox):
        super().apply_overlay(bbox)

    def initial_draw(self):
        for agent in self.agents:
            player = agent.player
            while len(player.hand) < 3:
                player.hand.add(self.game.draw())

    def play(self):
        ambushed = False
        if len(self.active_actions) == 0:
            self.active_agent = (self.active_agent + 1) % len(self.agents)
            agent = self.agents[self.active_agent]
            # print("NewAgent", agent.player.name)
            self.active_actions = [action for action in agent.turn()]
            ambushed = False
        if len(self.active_actions) > 0:
            action, self.active_actions = self.active_actions[0], self.active_actions[1:]
            if (action != None) and (len(action) > 0):
                agent = self.agents[self.active_agent]
                action, arguments = action[0], action[1:]
                # print(agent.player.name, "Action", action)
                if (action == "Discard") and not ambushed:
                    card = arguments[0]
                    self.discard(agent.player, card)
                    # print(agent.player.name, "Discard", card.name, len(agent.player.hand))
                if action == "Move":
                    location, exit = arguments
                    if not self.move_player(agent.player, location, exit):
                        self.active_actions = []
                if action == "Shortcut":
                    location, exit = arguments
                    self.move_player(agent.player, location, exit)
                    self.active_actions = []
                if action == "Challenge":
                    card, other_player = arguments
                    self.challenge(agent.player, card, other_player)
                    self.active_actions = []
                if action == "Finished":
                    location = arguments[0]
                    self.finished(agent.player, location)
                    self.active_actions = []
                    self.game.winner = agent.player
            if len(self.active_actions) == 0:
                # end of player move.
                agent = self.agents[self.active_agent]
                space = self.game.board.spaces[agent.player.location] if agent.player.location != None else None
                # if player was already ambushed turn ends no matter where they land
                if (space != None) and not ambushed:
                    if (space.level == 1):
                        # Ambush
                        player_card, monster_card = self.ambush_space(agent, space)
                        self.active_actions = [action for action in agent.turn(player_card)]
                        ambushed = True
                    else:
                        others = [player for player in self.players_at_location(agent.player.location)
                                if player != agent.player]
                        other_player = random.choice(others) if len(others) > 0 else None
                        if other_player != None:
                            self.share_space(agent.player, other_player)

    def ambush_space(self, agent: ff.Agent, space: bg.Space):
        # draw a card from players hand, and replace with one from draw_pile
        # draw a card from the draw_pile
        # if player >= monster, win, move forward player card value
        # else lost, move backward monster card value
        # Turn ends after an ambush (no second ambush or card share)
        player = agent.player
        player_card = self.game.discard(player.hand.draw(), name=player.name)
        agent.player.hand.add(self.game.draw(name=player.name))
        monster_card = self.game.discard(self.game.draw(name="monster"), name="monster")
        if player_card.value >= monster_card.value:
            print(player.name, "survives ambush by", monster_card.name)
            # move forward player_card.value spaces
            # agent.moves(shortcuts=False, Challenges=False)
        else:
            print(player.name, "hurt in ambush by", monster_card.name)
            # Move back monster_card.value spaces
        return player_card, monster_card
        
    def share_space(self, player, other_player):
        all_cards = [*player.hand, *other_player.hand]
        print("ShareCards", 
              player.name, len(player.hand), 
              other_player.name, len(other_player.hand))
            
        player.hand.remove_all()
        other_player.hand.remove_all()
        if len(all_cards) != 6:
            print("UhOh!  Somebody does not have three cards", 
                  player.name, len(player.hand), 
                  other_player.name, len(other_player.hand))
            exit()
        random.shuffle(all_cards)
        for card in all_cards[:3]:
            player.hand.add(card)
        for card in all_cards[3:]:
            other_player.hand.add(card)
                
    def players_at_location(self, location):
        return[agent.player for agent in self.agents
               if agent.player.location == location]
            
    def discard(self, player: ff.Player, card: bg.Card):
        player.hand.remove(card)
        self.game.discard(card, name=player.name)
        return True
    
    def move_player(self, player: ff.Player, location, exit: bg.Exit):
        player.location = exit.destination
        return True
    
    def challenge(self, challenger: ff.Player, challenger_card: ff.Card, 
                  challengee: ff.Player,
                 ):
        challengee_card: ff.Card = challengee.hand.draw(remove=True)
        self.game.discard(challengee_card, name=challengee.name)
        challengee.hand.add(self.game.draw(name=challengee.name))
        print(challenger.name, "challenges", challengee.name)
        if challenger_card.value >= challengee_card.value:
            forwards = self.game.forward_exits_for_location(challengee.location)
            if len(forwards) > 0:
                challenger.location = random.choice(forwards).destination
        
    def finished(self, player: ff.Player, location):
        player.location = None
        print("{} finished! {}".format(player.name, location))

    def update(self):
        if self.game.winner == None:
            self.play()
            self.resize()
            self.root.after(150, self.update)  # call update again after 1/2 second

    def run(self):
        self.update()
        self.root.mainloop()

    @property
    def json_path(self):
        return os.path.join(self.data_path, self.name + ".json")

    @property
    def image_path(self):
        return os.path.join(self.data_path, self.name + ".jpg")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print("Here", here)
    data_path = os.path.join(here, "../fafo/data")
    gv = GamePlayer("fafo", data_path)
    gv.run()