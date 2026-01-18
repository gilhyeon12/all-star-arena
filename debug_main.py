from game.main import Game
from game.settings import *
import pygame

class DebugGame(Game):
    def __init__(self):
        super().__init__()
        # Bypass menu
        self.game_mode = "2P"
        self.player1_char = "Naruto"
        self.player2_char = "Bleach"
        self.init_battle()
        self.state = STATE_BATTLE
        
        # Give mana for testing
        self.player1.mana = 50

if __name__ == "__main__":
    game = DebugGame()
    game.run()
