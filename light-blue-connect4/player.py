import random

class Player():

    def __init__(self, player_number, player_type):

        # Player number is either 1 or 2
        self.player_number = player_number

        # Player type is either "human" or "computer"
        self.player_type = player_type

    def getNumber(self):
        return self.player_number

    def getType(self):
        return self.player_type

    def getHumanMove(self, valid_moves):
        print("Valid moves: ", valid_moves)
        move = int(input("Player " + str(self.player_number) + " move: "))
        while move not in valid_moves:
            move = int(input("Invalid move. Player " + str(self.player_number) + " move: "))
        return move

    def getRandomMove(self, valid_moves):
        random_move = random.choice(valid_moves)
        return random_move

    def getComputerMove(self, board, valid_moves):
        random_move = random.choice(valid_moves)
        return random_move

    def getMove(self, board, valid_moves):
        if self.player_type == "human":
            return self.getHumanMove(valid_moves)
        elif self.player_type == "smart":
            return self.getComputerMove(board, valid_moves)
        else:   
            return self.getRandomMove(valid_moves)
    