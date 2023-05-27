
from game_logic import GameLogic

class Game:
    def __init__(self):
        self.logic = GameLogic()
        self.logic.reset()

    def play(self, max_round = 1):
        while self.logic.total_score < 10000 and self.logic.game_state != "exit_game" and self.logic.current_round <= max_round:
            self.logic.game_iteration()

        if self.logic.game_state != "exit_game":
            self.logic.game_iteration("quit_game")



if __name__ == "__main__":
       game = Game()
       game.play(2)