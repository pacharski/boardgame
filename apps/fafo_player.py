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
        if len(self.active_actions) == 0:
            self.active_agent = (self.active_agent + 1) % len(self.agents)
            agent = self.agents[self.active_agent]
            self.active_actions = [action for action in agent.turn()]
        if len(self.active_actions) > 0:
            action, self.active_actions = self.active_actions[0], self.active_actions[1:]
            if (action != None) and (len(action) > 0):
                agent = self.agents[self.active_agent]
                action, arguments = action[0], action[1:]
                if action == "Move":
                    location, exit = arguments
                    if not self.move_player(agent.player, location, exit):
                        self.active_actions = []
                if action == "Shortcut":
                    location, exit = arguments
                    self.move_player(agent.player, location, exit)
                    self.active_actions = []
                if action == "Challenge":
                    other_player = arguments[0]
                    self.challenge(agent.player, other_player)
                    self.active_actions = []
                if action == "Finished":
                    location = arguments[0]
                    self.finished(agent.player, location)
                    self.active_actions = []
                
    def move_player(self, player: ff.Player, location, exit: bg.Exit):
        player.location = exit.destination
        return True
    
    def challenge(self, challenger: ff.Player, challengee: ff.Player):
        print("{} challenges {}".format(challenger.name, challengee.name))

    def finished(self, player: ff.Player, location):
        player.location = None
        print("{} finished! {}".format(player.name, location))

    def update(self):
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