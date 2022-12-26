# Author: Jonathan Bergen
# Description: Defines the enviroment for the connect 4 game.

import random
import player
import pygame as pg
import time

# The connect 4 enviroment
class Enviroment():

    def __init__(self, mode="train"):

        # the game mode
        self.mode = mode

        # the pygame window size
        self.width = 700
        self.height = 600
        self.screen = pg.display.set_mode((self.width, self.height))

        # the board size
        self.nRows = 6
        self.nColumns = 7
        self.board = []
        
        # fill the board with 0's
        for i in range(6):
            self.board.append([0, 0, 0, 0, 0, 0, 0])

        # the players
        self.players = []

        # the settings and loops for the graphical version
        if self.mode == "test":
            self.running = True
            while self.running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False

    # reset the board
    def reset(self):
        self.board = []
        for i in range(6):
            self.board.append([0, 0, 0, 0, 0, 0, 0])
        return self.board


    ########################################
    # The following functions are for printing

    # terminal display
    def display(self):
        for row in self.board:
            for i in row:
                print(i, end=" ")
            print()


    # pygame display
    def drawScreen(self):
        
        self.screen.fill((16, 16, 164))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
 
        # draw the pieces
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.board[i][j] == 1:
                    pg.draw.circle(self.screen, (198, 30, 19), (int(cellWidth * j + cellWidth / 2), int(cellHeight * i + cellHeight / 2)), int(cellWidth / 2 - 5))
                if self.board[i][j] == 2:
                    pg.draw.circle(self.screen, (218, 199, 27), (int(cellWidth * j + cellWidth / 2), int(cellHeight * i + cellHeight / 2)), int(cellWidth / 2 - 5))

        pg.display.flip()


    ########################################
    # The following functions are for returning self values

    def getBoard(self):
        return self.board

    def getPlayers(self):
        return self.players


    ########################################
    # The following functions are for checking the state of the game

    def checkReward(self, pos, p_num):

        # reward amounts:
        # 0.1 for 1 adjacent tile
        # 0.3 for 2 adjacent tiles
        # 10 for 3 adjacent tiles
        # -5 for a tie game
        # -10 for a loss

        rewards = {}
        rewards[0] = 0
        rewards[1] = 0.1
        rewards[2] = 0.3
        rewards[3] = 10
        rewards[4] = 10
        rewards[5] = 10
        rewards[6] = 10

        # short hand names for row, columnm and board
        r, c = pos
        b = self.board
        reward = 0

        # check vertical
        v_score = 0
        for i in range(1, 4):
            try:
                tile_value = b[r + i][c]
                if tile_value == p_num:
                    v_score += 1
                else:
                    break
            except IndexError:
                break

        # check horizontal
        h_score = 0

        # going to the right
        for i in range(1, 4):
            try:
                tile_value = b[r][c + i]
                if tile_value == p_num:
                    h_score += 1
                else:
                    break
            except IndexError:
                break

        # going to the left
        for i in range(1, 4):
            try:
                tile_value = b[r][c - i]
                if tile_value == p_num and c > -1:
                    h_score += 1
                else:
                    break
            except IndexError:
                break
        
        # check down-left to up-right diagonal
        dl_to_ur_diagonal_score = 0

        # going down-left
        for i in range(1, 4):
            try:
                tile_value = b[r + i][c - i]
                if tile_value == p_num and c > -1:
                    dl_to_ur_diagonal_score += 1
                else:
                    break
            except IndexError:
                break

        # going up-right
        for i in range(1, 4):
            try:
                tile_value = b[r - i][c + i]
                if tile_value == p_num and r > -1:
                    dl_to_ur_diagonal_score += 1
                else:
                    break
            except IndexError:
                break

        # check up-left to down-right diagonal
        ul_to_dr_diagonal_score = 0

        # going up-left
        for i in range(1, 4):
            try:
                tile_value = b[r - i][c - i]
                if tile_value == p_num and r > -1 and c > -1:
                    ul_to_dr_diagonal_score += 1
                else:
                    break
            except IndexError:
                break

        # going down-right
        for i in range(1, 4):
            try:
                tile_value = b[r + i][c + i]
                if tile_value == p_num:
                    ul_to_dr_diagonal_score += 1
                else:
                    break
            except IndexError:
                break

        # calculate reward
        reward += rewards[v_score]
        reward += rewards[h_score]
        reward += rewards[dl_to_ur_diagonal_score]
        reward += rewards[ul_to_dr_diagonal_score]


        # Debugging

        # print("\n\nscore for player ", p_num, ":")
        # print("playing at:")
        # print("row: ", r, "column: ", c)
        # print("v_score: ", v_score)
        # print("h_score: ", h_score)
        # print("dl_to_ur_diagonal_score: ", dl_to_ur_diagonal_score)
        # print("ul_to_dr_diagonal_score: ", ul_to_dr_diagonal_score)
        # print("reward: ", reward)
        # self.display()
        # print("\n\n")

        return reward


    def isNotFull(self):
        for row in self.board:
            for i in row:
                if i == 0:
                    return True
        return False


    ########################################
    # The following functions are for making moves

    def getValidMoves(self):
        valid_moves = []
        for i in range(7):
            if self.board[0][i] == 0:
                valid_moves.append(i)
        return valid_moves

    def tryMove(self, move, player_num):
        for i in range(5, -1, -1):

            # if the move is valid, make the move and check the reward
            if self.board[i][move] == 0:
                self.board[i][move] = player_num
                reward = self.checkReward((i, move), player_num)

                # if the reward is 10, the player has won
                if reward >= 10:
                    print("Player", player_num, "wins!")
                    return self.board, reward, True

                # continue the game
                else:
                    return self.board, reward, False

            # if the top row of the board matrix is full, the game is tied
            if 0 not in self.board[0]:
                print("Tie game")
                return self.board, -5, True

        print("Error, it shouldn't get here")
        print("Tried to make move", move, "for player", player_num)
        self.display()