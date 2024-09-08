import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here)

from fafo.src.game import GameAction, Game
from fafo.src.player import Player
from fafo.src.card import Card, Deck
from fafo.src.board import Board, Space
from fafo.src.agent import Agent
from fafo.src.game_view import GameView
# from fafo.src.table_view import TableView
from fafo.src.qtrainer import QTrainer, Linear_QNet