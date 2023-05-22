import random

class GameLogic:

# Private
    #helper methods
    #V1
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
    
    #V2
    @staticmethod
    def __play_prompt():
        print("Welcome to Ten Thousand\n(y)es to play or (n)o to decline")
        while GameLogic.game_state == "play_prompt":

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
            if GameLogic.__check_zilch():
                GameLogic.__print_zilch()
                print(GameLogic.__check_zilch())
                GameLogic.current_round += 1
                continue
            print("Enter dice to keep, or (q)uit")
            GameLogic.__get_dice()
                       
    @staticmethod
    def __play_round():
        round_score = 0
        while GameLogic.game_state == "play_round":
            remaining = 6 if GameLogic.__check_hot_dice() else 6 - len(GameLogic.played_dice)

            print(f"You have {round_score + GameLogic.calculate_score(GameLogic.played_dice)} unbanked points and " + 
                f"{remaining} dice remaining")
            print("(r)oll again, (b)ank your points or (q)uit")
            choice= input("> ")
            if choice == 'b':
                round_score += GameLogic.calculate_score(GameLogic.played_dice)
                GameLogic.total_score += round_score
                print(f"You banked {round_score} points in round {GameLogic.current_round}\n"+
                        f"Total score is {GameLogic.total_score} points")
                GameLogic.current_round += 1
                GameLogic.played_dice = []
                GameLogic.game_state = "play_game"

            elif choice == 'r':
                print(f"Rolling {remaining} dice...\n***{list(GameLogic.roll_dice(remaining))}***")
                if GameLogic.__check_zilch():
                    GameLogic.__print_zilch()
                    GameLogic.current_round += 1
                    GameLogic.played_dice = []
                    GameLogic.game_state = "play_game"
                else:
                    
                    if remaining == 6:
                        round_score += GameLogic.calculate_score(GameLogic.played_dice)
                        GameLogic.played_dice = []
                    print("Enter dice to keep, or (q)uit")
                    GameLogic.__get_dice()

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
    
    #V3
    @staticmethod
    def __check_zilch():
        if len(GameLogic.current_roll) != 6:
            return GameLogic.calculate_score(GameLogic.current_roll + tuple(GameLogic.played_dice)) == GameLogic.calculate_score(GameLogic.played_dice)
        return GameLogic.calculate_score(GameLogic.current_roll) == 0

    @staticmethod
    def __print_zilch():
        print("""
****************************************
**        Zilch!!! Round over         **
****************************************""")
        print(f"You banked 0 points in round {GameLogic.current_round}\nTotal score is {GameLogic.total_score} points") 
         
    @staticmethod
    def __check_hot_dice():
        return len(GameLogic.get_scorers(GameLogic.played_dice)) == 6 and len(GameLogic.played_dice) == 6

    @staticmethod
    def __check_cheater_or_typo(dice):
        if GameLogic.__represents_int(dice):
            if GameLogic.validate_keepers(GameLogic.current_roll, dice):
                return True
        return False

    @staticmethod
    def __get_dice(return_state = "play_round"):
        while True:         
            choice= input("> ")
            if choice == "q":
                print(f"Thanks for playing. You earned {GameLogic.total_score} points")
                GameLogic.game_state = "quit_game"
                return
                    
            elif(GameLogic.__check_cheater_or_typo(choice)):
                GameLogic.played_dice += list(choice)
                GameLogic.game_state = return_state
                return
            else:
                print(f"Cheater!!! Or possibly made a typo...\n***{list(GameLogic.current_roll)}***")

    
    #helper methods
# Private


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
            raise Exception(f"number of dice {len(dice)} is out of bounds [1 , 6]")

        counts = [0] * 7  # initialize a counter for each possible value of a die
        for die in dice:
            if int(die) not in range(1, 7):
                raise Exception(f"die value {int(die)} is out of range [1 , 6]")
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
            raise Exception(f"number of dice {n} is out of bounds [1 , 6]")
        GameLogic.current_roll= tuple([random.randint(1, 6) for i in range(n)])

        return GameLogic.current_roll

    @staticmethod
    def play():
        while GameLogic.total_score <10000 and GameLogic.game_state != "quit_game":
            GameLogic.__game_iteration()

    @staticmethod
    def validate_keepers(roll, keepers):
        roll = [int(num) for num in roll]
        keepers = [int(num) for num in keepers]

        for die in keepers:
            if keepers.count(die) > roll.count(die):
                return False
        return True

    @staticmethod
    def get_scorers(dice):
        counts = [0] * 7  # initialize a counter for each possible value of a die
        for die in dice:
            counts[int(die)] += 1

        GameLogic.__triplets(counts)
        GameLogic.__three_pair(counts)
        GameLogic.__straight(counts)
        GameLogic.__singles(counts)

        reminder = []
        for count, i in enumerate(counts):
            reminder += [count] * i
        return tuple([item for item in dice if item not in reminder])

# Public

if __name__ == "__main__":
       GameLogic.play()

"""
    A class representing the logic for a game called Ten Thousand.

    Public Methods:
        - calculate_score(dice): Calculates the score based on the given dice values.
        - roll_dice(n): Rolls the specified number of dice and returns their values.
        - play(): Starts the game and manages the game state until a winning condition is met.
        - validate_keepers(roll, keepers): Validates the selected dice keepers based on the current roll.
        - get_scorers(dice): Returns the dice that contribute to the score.

    Attributes:
        - current_roll: Stores the current roll of dice.
        - total_score: Keeps track of the total score of the player.
        - current_round: Represents the current round number.
        - played_dice: Stores the dice that have been played in the current round.
        - game_state: Represents the current state of the game.

    Private Methods:
        - __represents_int(string): Helper method to check if a string represents an integer.
        - __empty_counts(counts): Helper method to reset the counts list to zero.
        - __triplets(counts): Helper method to calculate the score for triplets.
        - __three_pair(counts): Helper method to calculate the score for three pairs.
        - __singles(counts): Helper method to calculate the score for individual dice.
        - __straight(counts): Helper method to calculate the score for a straight sequence.
        - __play_prompt(): Helper method to prompt the player to start the game.
        - __check_zilch(): Helper method to check if the current roll results in a zilch.
        - __print_zilch(): Helper method to print the zilch message and update the round score.
        - __check_hot_dice(): Helper method to check if the player has rolled all scoring dice.
        - __check_cheater_or_typo(dice): Helper method to validate the user's input for dice selection.
        - __get_dice(return_state): Helper method to get the dice input from the player.
        - __play_game(): Helper method to handle the game flow during the "play_game" state.
        - __play_round(): Helper method to handle the game flow during the "play_round" state.
        - __game_iteration(): Helper method to execute the appropriate game logic based on the current game state.
"""
