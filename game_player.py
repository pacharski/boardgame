from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import tkinter

import a_game as ag
import board_game as bg


class GamePlayer(ag.GameView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.game = ag.Game.from_json_path(self.json_path)
        self.game.save_to_json_path(json_path="newgame.json")
        self.agents = [bg.Agent(player, self.game.board) for player in self.game.players]
        self.active_agent = -1
        self.active_actions = []
        
        self.root = tkinter.Tk()
        self.root.title("Game Player")
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

    def play(self):
        if len(self.active_actions) == 0:
            self.active_agent = (self.active_agent + 1) % len(self.agents)
            agent = self.agents[self.active_agent]
            self.active_actions = [action for action in agent.turn()]
        if len(self.active_actions) > 0:
            action, self.active_actions = self.active_actions[0], self.active_actions[1:]
            if (action != None) and (len(action) > 0):
                agent = self.agents[self.active_agent]
                if action[0] == "move":
                    location, barrier, destination = action[1:]
                    agent.player.location = destination
                    
    def update(self):
        self.play()
        self.resize()
        self.root.after(50, self.update)  # call update again after 1/2 second

    def run(self):
        self.update()
        self.root.mainloop()

    @property
    def json_path(self):
        return os.path.join(self.data_path, self.name + ".json")

    @property
    def image_path(self):
        return os.path.join(self.data_path, self.name + ".png")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "data")
    gv = GamePlayer("game", data_path)
    gv.run()