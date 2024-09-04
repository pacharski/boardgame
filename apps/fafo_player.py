from pathlib import Path
# print('Running' if __name__ == '__main__' else
#       'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(here))

import tkinter
import random
import fafo as ff
import board_game as bg


class PlayerStats():
    def __init__(self):
        self.move_count = 0
        self.challenge_count = 0

    def move(self):
        self.move_count += 1

    def challenge(self):
        self.challenge_count += 1

    def __str__(self):
        form="Moves={}, Challenges={}"
        return form.format(self.move_count, self.challenge_count)


class GamePlayer(ff.GameView):
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.game = ff.Game(self.name, self.data_path)
        self.winner = None

        # disable all but 4 players
        for pid in range(4, len(self.game.players)):
            self.game.players[pid].location = None
        self.agents = [ff.Agent(player, self.game) 
                       for player in self.game.players if player.location != None]
        self.active_agent = -1
        self.active_actions = []

        self.stats = {agent: PlayerStats() for agent in self.agents}

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

    def print_action_summary(self, agent, actions):
        # collect stats on what each player choose to do
        # print summary of move selected for player
        card, destination, challengee = None, None, None
        for action in actions:
            if action.action == "Discard":
                card = action.card.name
            elif action.action == "Move":
                destination = action.location
            elif action.action == "Challenge":
                challengee = action.other_player.name
        if destination != None:
            self.stats[agent].move()
            print(agent.player.name, agent.player.marker.color, card, 
                  "move", destination)
        elif challengee != None:
            self.stats[agent].challenge()
            print(agent.player.name, agent.player.marker.color, card, 
                  "challenge", challengee)
        else:
            print(agent.player.name, agent.player.marker.color, card, 
                  "unknown")

    def play(self):
        if len(self.active_actions) == 0:
            # Next player
            if self.winner != None:
                return
            self.active_agent = (self.active_agent + 1) % len(self.agents)
            agent = self.agents[self.active_agent]
            self.active_actions = agent.choose_action()
            self.print_action_summary(agent, self.active_actions)
        if len(self.active_actions) > 0:
            action, self.active_actions = self.active_actions[0], self.active_actions[1:]
            if (action != None):
                agent = self.agents[self.active_agent]
                if (action.action == "Discard"):
                    # print(action.player.name, "discard", action.card.name)
                    self.discard(agent.player, action.card)
                elif action.action == "Move":
                    if not self.move_player(agent.player, action.location):
                        self.finished(agent.player, action.location)
                        self.active_actions = []
                elif action.action == "Challenge":
                    self.challenge(agent.player, action.card, action.other_player)
                elif action.action == "Final":
                    # end of player move after ambush advance/retreat
                    pass
                elif action.action == "SpaceAction":
                    # print("FafoPlayerSpaceAction")
                    # end of player move.
                    agent = self.agents[self.active_agent]
                    space = self.game.board.spaces[agent.player.location] if agent.player.location != None else None
                    # if player was already ambushed turn ends no matter where they land
                    if (space != None):
                        # print("FafoPlayerValidSpace")
                        if (space.level == 1):
                            # Ambush
                            # print("FafoPlayerAmbush")
                            self.active_actions = self.ambush(agent, space)
                            self.print_action_summary(agent, self.active_actions)
                        else:
                            # print("FafoPlayerShare")
                            # Share cards with other player in same space
                            self.share_space(agent)
                        
    def ambush(self, agent: ff.Agent, space: bg.Space):
        # draw a card from players hand, and replace with one from draw_pile
        # draw a card from the draw_pile
        # if player >= monster, win, move forward player card value
        # else lost, move backward monster card value
        # Turn ends after an ambush (no second ambush or card share)
        player = agent.player
        player_card = agent.choose_card_for_ambush()
        self.game.discard(player_card, name=player.name)
        player.hand.add(self.game.draw(name=player.name))
        monster_card = self.game.discard(self.game.draw(name="monster"), name="monster")
        if player_card.value >= monster_card.value:
            # print(player.name, "survives ambush by", monster_card.name)
            return [action for action 
                    in agent.choose_action_after_ambush_win(player_card)]
        else:
            # print(player.name, "hurt in ambush by", monster_card.name)
            return [action for action 
                    in agent.choose_action_after_ambush_loss(player_card)]                            
        
    def share_space(self, agent):
        other_players = [player
                         for player in self.players_at_location(agent.player.location)
                         if player != agent.player]
        if len(other_players) == 0:
            return False
        
        other_player = agent.choose_player_to_share_cards(other_players)
        all_cards = [*agent.player.hand, *other_player.hand]
        # print("ShareCards", 
        #       agent.player.name, len(agent.player.hand), 
        #       other_player.name, len(other_player.hand))
        if len(all_cards) != 6:
            print("UhOh!  Somebody does not have three cards", 
                  agent.player.name, len(agent.player.hand), 
                  other_player.name, len(other_player.hand))
            exit()
        keep_cards, return_cards = agent.choose_shared_cards_to_keep(all_cards, other_player)
        agent.player.hand.remove_all()
        for card in keep_cards:
            agent.player.hand.add(card)
        other_player.hand.remove_all()
        for card in return_cards:
            other_player.hand.add(card)
        return True
        
    def players_at_location(self, location):
        return[agent.player for agent in self.agents
               if agent.player.location == location]
            
    def discard(self, player: ff.Player, card: bg.Card):
        player.hand.remove(card)
        self.game.discard(card, name=player.name)
        return True
    
    def move_player(self, player: ff.Player, destination: int):
        player.location = destination
        return len(self.game.forward_exits_for_location(destination)) > 0
    
    def challenge(self, challenger: ff.Player, challenger_card: ff.Card, 
                  challengee: ff.Player,
                 ):
        challengee_card: ff.Card = challengee.hand.draw(remove=True)
        self.game.discard(challengee_card, name=challengee.name)
        challengee.hand.add(self.game.draw(name=challengee.name))
        # print(challenger.name, "challenges", challengee.name)
        if challenger_card.value >= challengee_card.value:
            forwards = self.game.forward_exits_for_location(challengee.location)
            if len(forwards) > 0:
                challenger.location = random.choice(forwards).destination
        
    def finished(self, player: ff.Player, location):
        player.location = None
        self.winner = player
        print("{} finished! {}".format(player.name, location))
        for agent in self.agents:
            print(agent.player.name, str(self.stats[agent]))

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