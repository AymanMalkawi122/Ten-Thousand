import random

class GameLogic:

# Private

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
        print(counts,"22222222")
        counts[1] = 0
        counts[5] = 0

        return score

    @staticmethod
    def __straight(counts):
        if all(counts[1:7]):  
            GameLogic.__empty_counts(counts)
            return 1500
        
        return 0

# Public
    @staticmethod
    def calculate_score(dice):
        score = 0

        if len(dice) > 6:
            raise Exception("number of dice is out of bounds [1 , 6]")

        counts = [0] * 7  # initialize a counter for each possible value of a die
        for die in dice:
            if(die not in range(1, 7)):
                raise Exception("die value is out of range [1 , 6]")
            counts[die] += 1
       
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
        numbers = [random.randint(1, 6) for i in range(n)]
        return tuple(numbers)

"""
This class provides game logic for calculating the score of a roll of dice
and for rolling a certain number of dice. The scoring system is based on the
following rules:

1. Triples - Three dice with the same number, except for three 1's which are worth 1000 points.
2. Three pairs - A roll with three pairs of different numbers. This is worth 1500 points.
3. Straight - A roll with all six dice showing different numbers in sequence. This is worth 1500 points.
4. Singles - Any dice that is not part of a triple, pair or straight and shows 1 or 5. 
   Ones are worth 100 points each and fives are worth 50 points each.

Public methods:

- calculate_score(dice): Calculates the score of a roll of dice according to the above rules.
- roll_dice(n): Rolls a certain number of dice and returns the values as a tuple.

Private methods:

- __empty_counts(counts): Resets the counts of dice in each category to 0.
- __triplets(counts): Calculates the score for any triplets in the roll.
- __three_pair(counts): Calculates the score for any three pairs in the roll.
- __singles(counts): Calculates the score for any single 1's or 5's in the roll.
- __straight(counts): Calculates the score for a straight roll of all six dice.
"""