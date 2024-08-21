from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import tkinter
import random

import a_game as ag
import board_game as bg


class GamePlayer(ag.GameView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.game = ag.Game.from_json_path(self.json_path)
        # disable all but 4 players
        for pid in range(4, len(self.game.players)):
            self.game.players[pid].location = None
        self.agents = [bg.Agent(player, self.game.board, self.game.players) 
                       for player in self.game.players if player.location != None]
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
                action, location, exit = action
                if action == "Move":
                    self.move_player(agent.player, location, exit)
                elif action == "Encounter":
                    self.encounter(agent.player, location, exit)
                elif action == "SecretDoor":
                    self.secret_door(agent.player, location, exit)

    def move_player(self, player, location, exit):
        if exit.barrier == "Secret Door":
            print("Try to find secret door")
            # Abortplayer.location = destination
        player.location = exit.destination
                    
    def encounter(self, player, location, exit):
        space = self.game.board.spaces[location]
        if (space.name == "Room"):
            if (space.num_encounters == 0):        
                print("Setup new Room encounter for", player.name, location)
                space.encounters.append(("Adversary", "Reward", player))
            else:
                adversary, reward, assigned = space.encounters[0]
                if adversary != None:
                    print("Takeover Room encounter for", player.name, location)
                    space.encounters[0] = (adversary, reward, player)
                else:
                    #No Encounter
                    pass
        elif (space.name != "") and (space.id != 92) and (space.id != 93):
            # big room
            if (space.num_encounters == 0):
                print("Setup new BigRoom encounter for", player.name, location)
                space.encounters.append(("Adversary", "Rewards", player))
            else:
                got_one = False
                for encounter in space.encounters:
                    adversary, reward, assigned = encounter
                    if assigned == None:
                        print("Takeover BigRoom encounter for", player.name, location)
                        encounter = (adversary, reward, player)
                        got_one = True
                        break
                if not got_one:
                    print("Setup new BigRoom encounter for", player.name, location)
                    space.encounters.append(("Adversary", "Rewards", player))
    
    def secret_door(self, player: bg.Player, location, exit: bg.Exit):
        if exit.barrier != "Secret Door":
            print("ExitIsNotSecretDoor!!!")            
            return
        if player in exit.open:
            # already found
            return True
        # FIXME add magic item to find secret doors
        print("Try to find secret door", exit)
        roll = random.randint(1, 6)
        if ((roll < 3)
            or (player.desc == "Elf") and (roll < 5)):
            # found it!
            exit.open.add(player)
            return True
        else:
            return False
             
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
        return os.path.join(self.data_path, self.name + ".png")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "data")
    gv = GamePlayer("game", data_path)
    gv.run()