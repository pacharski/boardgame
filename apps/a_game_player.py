from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(here))

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
        self.agents = [ag.Agent(player, self.game.board, self.game.players) 
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
                    if not self.move_player(agent.player, location, exit):
                        self.active_actions = []
                elif action == "Encounter":
                    self.encounter(agent.player, location, exit)
                elif action == "SecretDoor":
                    self.secret_door(agent.player, location, exit)

    def move_player(self, player, location, exit):
        if exit.barrier == "Secret Door":
            if player not in exit.open:
                # secret door is not found, cannot go through
                print("Secret Door is not found", player.name, exit)
                return False
        player.location = exit.destination
        return True

    def getAdversary(self, level):
        adversaries = [creature for creature in self.game.horde if creature.level == level]
        if len(adversaries) > 0:
            return random.choice(adversaries)
        
    def getReward(self, level):
        rewards = [treasure for treasure in self.game.hoard if treasure.level == level]
        if len(rewards) > 0:
            reward = random.choice(rewards)
            self.game.hoard = [treasure for treasure in self.game.hoard if treasure != reward]
            return reward
                    
    def encounter(self, player, location, exit):
        space = self.game.board.spaces[location]
        if (space.name == "Room"):
            if (space.num_encounters == 0):        
                adversary = self.getAdversary(space.level)
                reward = self.getReward(space.level)
                print("Setup new Room encounter for", player.name, location, 
                      adversary.desc, reward.desc)
                space.encounters.append((adversary, reward, player))
                self.fight_adversary(space, adversary, reward, player)
            else:
                adversary, reward, assigned = space.encounters[0]
                if adversary != None:
                    print("Takeover Room encounter for", player.name, location, 
                          adversary.desc)
                    space.encounters[0] = (adversary, reward, player)
                    self.fight_adversary(space, adversary, reward, player)
                else:
                    #No Encounter
                    pass
        elif (space.name != "") and (space.id != 92) and (space.id != 93):
            # big room
            if (space.num_encounters == 0):
                adversary = self.getAdversary(space.level)
                print("Setup new BigRoom encounter for", player.name, location, 
                      adversary.desc)
                space.encounters.append((adversary, None, player))
                self.fight_adversary(space, adversary, None, player)
            else:
                got_one = False
                for encounter in space.encounters:
                    adversary, reward, assigned = encounter
                    if assigned == None:
                        print("Takeover BigRoom encounter for", player.name, location, 
                              adversary.desc)
                        encounter = (adversary, reward, player)
                        self.fight_adversary(space, adversary, reward, player)
                        got_one = True
                        break
                if not got_one:
                    adversary = self.getAdversary(space.level)
                    print("Setup new BigRoom encounter for", player.name, location, 
                          adversary.desc)
                    space.encounters.append((adversary, None, player))
                    self.fight_adversary(space, adversary, None, player)

    def get_defense(self, adversary, player):
        defense = (adversary.defenses[0] if (player.desc == "Elf") else
                   adversary.defenses[1] if (player.desc == "Hero") else
                   adversary.defenses[2] if (player.desc == "Super Hero") else
                   adversary.defenses[3] if (player.desc == "Wizard") else
                   "13")
        return int(defense) if defense != "-" else 13

    def fight_adversary(self, space, adversary, reward, player):
        if adversary.desc.startswith("Trap"):
            pass # FIXME handle traps
        else:
            roll = random.randint(1, 6) + random.randint(1, 6)
            defense = self.get_defense(adversary, player)
            killed = roll >= defense
            if killed:
                if reward != None:
                    print("AddRewardToPlayer", reward, player.name)
                    player.hoard.add(reward)
                print(player.name, "killed", adversary.desc, "and won", 
                      reward.desc if reward != None else "nothing",
                      "total", player.hoard.value)
                space.encounter = (None, None, None)

    
    def secret_door(self, player: ag.Player, location, exit: bg.Exit):
        if exit.barrier != "Secret Door":
            print("ExitIsNotSecretDoor!!!")            
            return
        if player in exit.open:
            # already found
            return True
        return self.search_for_secret_door(exit, player)

    def search_for_secret_door(self, exit, player):
        # FIXME add magic item to find secret doors
        roll = random.randint(1, 6)
        found = (roll < 5) if (player.desc == "Elf") else (roll < 3)
        print("Search for secret door {}".format("found" if found else "not found"), exit)
        if found:
            exit.open.add(player)
        return found
             
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
    data_path = os.path.join(here, "../a_game/data")
    gv = GamePlayer("a_game", data_path)
    gv.run()