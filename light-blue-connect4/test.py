# AI for Games - Beat the Snake game
# Testing the AI

# Importing the libraries
import enviroment as env
from brain import Brain
import pygame as pg
import numpy as np
import random
import math

# Defining the parameters
nLastStates = 4
filepathToOpen = 'model_data/test1.h5'
slowdown = 75

# Creating the Environment and the Brain
env = env.Enviroment("test")
brain = Brain((6, 7, nLastStates))
model = brain.loadModel(filepathToOpen)


# Initializing the pygame window
env.drawScreen()

# Making a function that will reset game states
def resetStates():
    currentState = np.zeros((1, 6, 7, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.getBoard()
   
    return currentState, currentState

# Starting the main loop
while True:
    # Resetting the game and the game states
    env.reset()
    currentState, nextState = resetStates()
    gameOver = False
    
    # Playing the game
    while not gameOver: 

        # Choosing an action to play
        valid_moves = env.getValidMoves()

        # else, choose the action with the highest q-value, but only from the valid moves

        qvalues = model.predict(currentState)
        print("valid moves: ", valid_moves)
        print("qvalues: ", qvalues)
        
        # remove the q-values for invalid moves by setting invalid moves to negative infinity
        for i in range(7):
            if i not in valid_moves:
                qvalues[0][i] = -math.inf

        print("new qvalues: ", qvalues)
        action = np.argmax(qvalues[0])
        print("action: ", action)
        
        # Updating the environment

        # make the ai move
        state, reward_1, gameOver = env.tryMove(action, 1)
        
        # Adding new game frame to next state and deleting the oldest one from next state
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        # Updating current state
        currentState = nextState

        # Displaying the game
        env.drawScreen()
        env.display()

        # get the player's move, filtering for valid moves
        valid_moves = env.getValidMoves()
        action = None
        while action not in valid_moves:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        action = 0
                    if event.key == pg.K_2:
                        action = 1
                    if event.key == pg.K_3:
                        action = 2
                    if event.key == pg.K_4:
                        action = 3
                    if event.key == pg.K_5:
                        action = 4
                    if event.key == pg.K_6:
                        action = 5
                    if event.key == pg.K_7:
                        action = 6


        # make the player's move
        state, reward_2, gameOver = env.tryMove(action, 2)
        
       
        env.drawScreen()
        env.display()

        # Slow down the game
        pg.time.wait(slowdown)
