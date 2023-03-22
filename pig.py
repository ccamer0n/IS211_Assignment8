import random
import time
import argparse
random.seed(0)

class Dice():
    '''This class represents a single die of variable sides.'''
    def __init__(self, sides):
        self.sides = sides

class Player():
    '''This class represents a player for a dice-based game with methods to roll and hold.'''
    def __init__(self, name):
        self.name = name
    def roll(self, dice):
        return int('{:1.0f}'.format(random.uniform(1, dice.sides)))
    def hold(self, running_total):
        print(f"...\n{self.name}, you've added {running_total} to your score.")
        return running_total

class HumanPlayer(Player):
    def turn(self, running_total, score):
        choice = input(f"{self.name}, please enter 'r' to roll or 'h' to hold >>> ")
        return choice

class ComputerPlayer(Player):
    def turn(self, running_total, score):
        hold = min(25, (100 - score))
        if running_total < hold:
            return 'r'
        else:
            return 'h'

class PlayerFactory():
    def getPlayer(self, args):
        playerType = vars(args)
        if playerType['player1'] == 'human':
            player1 = HumanPlayer("Player 1")
        else:
            player1 = ComputerPlayer("Player 1")
        if playerType['player2'] == 'human':
            player2 = HumanPlayer("Player 2")
        else:
            player2 = ComputerPlayer("Player 2")
        return player1, player2

class Game():
    '''This is a class for the game Pig.
    It contains the rules and method to play.'''
    def __init__(self):
        self.name = "Pig"
        self.rules = '''The goal of Pig is to reach 100 points before the other player.
During your turn you may roll the die until either a 1 is rolled or until you choose to hold.
Holding scores the sum of rolls for that round. If a 1 is rolled, no points are received.'''

    def __str__(self):
        return f"This is a game called {self.name}."

    def play(self, args):
        '''This function instantiates class objects for players and dice.
        It calls the play method of the game Pig, changes turns, and prints the winner.'''
        factory = PlayerFactory()
        player1, player2 = factory.getPlayer(args)
        dice = Dice(6)
        p1_score = 0
        p2_score = 0
        print(f"***{self.name}***".center(93))
        print(f"{self.rules}\n")
        while p1_score < 100 and p2_score < 100:
            p1_score += int(self.turns(player1, p1_score, dice))
            print(f"Your total score is {p1_score}.\n")
            if p1_score >= 100:
                break
            p2_score += self.turns(player2, p2_score, dice)
            print(f"Your total score is {p2_score}.\n")
        if p1_score > p2_score:
            print(f"Congratulations {player1.name}! You've won!")
        else:
            print(f"Congratulations {player2.name}! You've won!")

    def turns(self, player, total_score, dice):
        '''This function manages the rules during player turns'''
        result = 0
        running_total = 0
        score = total_score
        choice = player.turn(running_total, score)
        while choice != 'r' and choice != 'h':
            choice = input("Invalid entry. Please enter 'r' to roll or 'h' to hold >>> ")
        while choice == 'r' and not result == 1 and not running_total >= 100:
            result = player.roll(dice)
            print(f"...\n{player.name} rolled a {result}.")
            if result == 1:
                running_total = 0
                return running_total
            else:
                running_total += result
                score = total_score + running_total
                print(f"The running total for this turn is {running_total}.")
                if running_total >= 100 or score >= 100:
                    return running_total
                else:
                    print(f"{player.name}'s total score is {score}.")
                    choice = player.turn(running_total, score)
                    while choice != 'r' and choice != 'h':
                        choice = input("Invalid entry. Please enter 'r' to roll or 'h' hold >>> ")
                    if choice == 'h':
                        return player.hold(running_total)
        if choice == 'h':
            return player.hold(running_total)

class TimedGameProxy(Game):
    '''This class adds a time limit to the game.'''
    def __init__(self):
        self.name = 'Pig'
        self.rules = '''The goal of Pig is to reach 100 points before the other player.
During your turn you may roll the die until either a 1 is rolled or until you choose to hold.
Holding scores the sum of rolls for that round. If a 1 is rolled, no points are received.'''

    def timedPlay(self, args):
        factory = PlayerFactory()
        player1, player2 = factory.getPlayer(args)
        dice = Dice(6)
        p1_score = 0
        p2_score = 0
        timeLimit = 10
        print(f"***{self.name}***".center(93))
        print(f"{self.rules}\n")
        startTime = time.time()
        while p1_score < 100 and p2_score < 100:
            if self.getTime(startTime) < timeLimit:
                p1_score += self.turns(player1, p1_score, dice)
                print(f"Your total score is {p1_score}.\n")
                if p1_score >= 100:
                    break
            else:
                print("Time's up!")
                break
            if self.getTime(startTime) < timeLimit:
                p2_score += self.turns(player2, p2_score, dice)
                print(f"Your total score is {p2_score}.\n")
            else:
                print("Time's up!")
                break
        if p1_score > p2_score:
            print(f"Congratulations {player1.name}! You've won!")
        else:
            print(f"Congratulations {player2.name}! You've won!")

    def getTime(self, startTime):
        currentTime = time.time()
        return currentTime - startTime


def main(args):
    '''This is the main function. It instantiates either a classic or timed game based on parameters'''
    params = vars(args)
    if params['timed'] == True:
        game = TimedGameProxy()
        game.timedPlay(args)
    else:
        game = Game()
        game.play(args)

if __name__ == "__main__":
    '''Main entry point'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', choices=['human', 'computer'], default='human')
    parser.add_argument('--player2', choices=['human', 'computer'], default='computer')
    parser.add_argument('-t', '--timed', default=False)
    args = parser.parse_args()
    main(args)