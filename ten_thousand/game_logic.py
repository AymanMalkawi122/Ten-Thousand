import random

class GameLogic:

# Private
    #helper methods
    @staticmethod
    def __represents_int(string):
        try: 
            int(string)
        except ValueError:
            return False
        else:
            return True
        
    @staticmethod
    def __empty_counts(counts):
        for i in range(1,7):
            counts[i] = 0

    @staticmethod
    def __triplets(counts):
        score = 0
        for i in range(1, 7):

            if counts[i] >= 3:
                if i == 1:
                    score+=(counts[i] - 2) * 1000
                    counts[i] = 0

                else:
                    score +=(counts[i] - 2) * (i * 100)
                    counts[i] = 0
        return score

    @staticmethod
    def __three_pair(counts):
        pairs = 0
        for i in range(1, 7):
            if counts[i] == 2:
                    pairs += 1

        if pairs == 3:
            GameLogic.__empty_counts(counts)
            return 1500
        return 0

    @staticmethod
    def __singles(counts):
        score = 0

        score += counts[1] * 100
        score += counts[5] * 50
        counts[1] = 0
        counts[5] = 0

        return score

    @staticmethod
    def __straight(counts):
        if all(counts[1:7]):
            GameLogic.__empty_counts(counts)
            return 1500

        return 0

    @staticmethod
    def __play_prompt():
        print("Welcome to Ten Thousand\n(y)es to play or (n)o to decline")
        while(GameLogic.game_state == "play_prompt"):

            choice= input("> ")
            if choice == "n":
                print("OK. Maybe another time")
                GameLogic.game_state = "quit_game"
            elif choice == "y":
                GameLogic.game_state = "play_game"
            else:
                print("wrong input!")

    @staticmethod
    def __play_game():
        while(GameLogic.game_state == "play_game"):
            print(f"Starting round {GameLogic.current_round}")
            print(f"Rolling 6 dice...\n***{list(GameLogic.roll_dice(6))}***")        
            print("Enter dice to keep, or (q)uit")

            choice= input("> ")
            if choice == "q":
                print(f"Thanks for playing. You earned {GameLogic.total_score} points")
                GameLogic.game_state = "quit_game"
                    
            elif(GameLogic.__represents_int(choice)):
                GameLogic.played_dice += list(choice)
                GameLogic.game_state = "play_round"
            else:
                print("wrong input!")

    @staticmethod
    def __play_round():
        while(GameLogic.game_state == "play_round"):
            
            print(f"You have {GameLogic.calculate_score(GameLogic.played_dice)} unbanked points and " + 
                f"{len(GameLogic.current_roll) - len(GameLogic.played_dice)} dice remaining")
            print("(r)oll again, (b)ank your points or (q)uit")
            choice= input("> ")
            if choice == 'b':
                GameLogic.total_score += GameLogic.calculate_score(GameLogic.played_dice)
                print(f"You banked {GameLogic.calculate_score(GameLogic.played_dice)} points in round {GameLogic.current_round}\n"+
                        f"Total score is {GameLogic.total_score} points")
                GameLogic.current_round += 1
                GameLogic.played_dice = []
                GameLogic.game_state = "play_game"

            elif choice == 'r':
                pass

            elif choice == 'q':
                print(f"Thanks for playing. You earned {GameLogic.total_score} points")
                GameLogic.game_state = "quit_game"

            else:
                print("wrong input!")

    @staticmethod
    def __game_iteration():
        state_map={
           "play_prompt" : GameLogic.__play_prompt,
           "play_game" : GameLogic.__play_game,
           "play_round" : GameLogic.__play_round,
        }
        state_map[GameLogic.game_state]()
    #helper methods

# Public

    current_roll = 0
    total_score = 0
    current_round = 1
    played_dice = []
    game_state = "play_prompt"

    @staticmethod
    def calculate_score(dice):
        score = 0

        if len(dice) > 6:
            raise Exception("number of dice is out of bounds [1 , 6]")

        counts = [0] * 7  # initialize a counter for each possible value of a die
        for die in dice:
            if(int(die) not in range(1, 7)):
                raise Exception("die value is out of range [1 , 6]")
            counts[int(die)] += 1

        # triplets and above
        score += GameLogic.__triplets(counts)
        # check for 3 pairs
        score += GameLogic.__three_pair(counts)
        # straight
        score += GameLogic.__straight(counts)
        # check for 1's and 5's
        score += GameLogic.__singles(counts)

        return score

    @staticmethod
    def roll_dice(n):

        if n not in range(1, 7):
            raise Exception("number of dice is out of bounds [1 , 6]")
        GameLogic.current_roll= tuple([random.randint(1, 6) for i in range(n)])

        return GameLogic.current_roll

    @staticmethod
    def play():
        while GameLogic.total_score <10000 and GameLogic.game_state != "quit_game":
            GameLogic.__game_iteration()


if __name__ == "__main__":
       GameLogic.play()

"""
    This class provides game logic functionalities for a dice game.

    Methods:
    - calculate_score(dice): Calculates the total score for a given set of dice.
    - roll_dice(n): Rolls a specified number of dice.
    - play(): Starts the game and manages the gameplay.

    Attributes:
    - current_roll: The current roll of dice.
    - total_score: The total score accumulated in the game.
    - current_round: The current round number.
    - played_dice: The dice that have been played in the current round.
    - game_state:  the state of the game
    Usage:
    - Use the play method to start the game and manage the gameplay.
"""