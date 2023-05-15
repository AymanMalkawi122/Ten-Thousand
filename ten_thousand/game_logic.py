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
    def __hood_dice(counts):
        pairs = 0
        for i in range(1, 7):
            if counts[i] == 2:
                    pairs += 1
        
        if pairs == 3:
            GameLogic.__empty_counts   
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

        counts = [0] * 7  # initialize a counter for each possible value of a die
        for die in dice:
            counts[die] += 1
       
        # triplets and above
        score += GameLogic.__triplets(counts)
        # check for 3 pairs 
        score += GameLogic.__hood_dice(counts)
        # straight
        score += GameLogic.__straight(counts)
        # check for 1's and 5's
        score += GameLogic.__singles(counts)   

        return score  
    
    @staticmethod
    def roll_dice(n):
        numbers = [random.randint(1, 6) for i in range(n)]
        return tuple(numbers)
    
print(GameLogic.calculate_score((1,2,3,4,5,6)))
print(GameLogic.calculate_score((1,1,4,4,6,6)))