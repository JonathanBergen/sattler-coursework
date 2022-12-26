# Author: Jonathan Bergen
# Description: Runs the game of connect 4.

import enviroment

def play(board):

    while board.isNotFull():

        # Alternates between player 1 and 2
        for player in [1, 2]:

            board.makeMove(player)
            board.display()

            if board.checkWin() != 0:
                print("Player " + str(player) + " wins!")
                return

    if board.checkWin() == 0:
        print("Tie game!")

def main():

    # Gets the game mode
    print("Welcome to Connect 4!")
    print("Choose a game mode:")
    print("1. Human vs. Human")
    print("2. Human vs. Computer")
    print("3. Computer vs. Computer")
    game_mode = int(input("Game mode: "))
    while game_mode not in [1, 2, 3]:
        game_mode = int(input("Invalid game mode. Game mode: "))

    # Creates the enviroment
    env = enviroment.Enviroment()
    env.display()

    # Creates the players
    env.addPlayers(game_mode)
    play(env)

if __name__ == "__main__":
    main()