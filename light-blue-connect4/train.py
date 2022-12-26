# This code is based on: AI for Games - Beat the Snake game
# I modified it to work with connect 4
# I also added a second AI to play against the first AI


# Importing the libraries
import enviroment
from brain import Brain
from DQN import Dqn
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Defining the parameters

# the memory size of the game: this is the amount of games that the AI will remember
memSize = 60000

# the batch size of the game: this is the amount of games that the AI will train on at a time
batchSize = 32

# the learning rate of the game: this is rate at which the AI trusts its own predictions
learningRate = 0.0001

# the discount factor of the game: this is the rate at which the AI values future rewards
gamma = 0.9

# the number of last states that the AI will remember
nLastStates = 4

# the number of epochs that the AI will train for. In this training system, an epoch is one full game
maxEpochs = 300

# epsilon represents the probability of the AI choosing a random action
# it starts at 1 and decays to 0.05, at a rate of 0.02 per epoch
# with every epoch, the AI becomes more confident in its predictions
epsilon = 1.0
epsilonDecayRate = 0.02
minEpsilon = 0.05

# the paths to save the models of each AI
filepathToSave1 = 'model_data/bleh1.h5'
filepathToSave2 = 'model_data/bleh2.h5'


# Creating the Environment, the Brain and the Experience Replay Memory
env = enviroment.Enviroment()
brain1 = Brain((6, 7, nLastStates), learningRate)
brain2 = Brain((6, 7, nLastStates), learningRate)
model1 = brain1.model
model2 = brain2.model
dqn1 = Dqn(memSize, gamma)
dqn2 = Dqn(memSize, gamma)

# Making a function that will initialize game states
def resetStates():
    currentState = np.zeros((1, 6, 7, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.getBoard()
    
    return currentState, currentState

# Starting the main loop
epoch = 0
p1_wins = 0
p2_wins = 0
n_ties = 0
game_history = []


while True:

    # Resetting the environment and game states
    env.reset()
    currentState1, nextState1 = resetStates()
    currentState2, nextState2 = resetStates()
    epoch += 1
    gameOver = False
    
    # Starting the second loop in which we play the game and teach our AI
    while not gameOver: 

        winner = None

        # Choosing an action to play
        valid_moves = env.getValidMoves()

        # if random float between 0 and 1 is less than epsilon, choose a random action
        if random.random() < epsilon:
            action1 = random.choice(valid_moves)

        # else, choose the action with the highest q-value
        else:
            qvalues = model1.predict(currentState1)
            print("p1 valid moves: ", valid_moves)
            print("p1 qvalues: ", qvalues)
        
        # remove the q-values for invalid moves by setting invalid moves to negative infinity
            for i in range(7):
                if i not in valid_moves:
                    qvalues[0][i] = -math.inf

            print("p1 new qvalues: ", qvalues)
            action1 = np.argmax(qvalues[0])
            print("p1 action: ", action1)
            


        # Updating the environment

        # make the ai player 1 move
        state1, reward_1, gameOver = env.tryMove(action1, 1)

        # check if player 1 won
        if reward_1 >= 10:
            winner = 1
            p1_wins += 1
            reward_2 = -6
            print("p1 wins")
            break

        # make the ai player 2 move
        if gameOver == False:

            # get the valid moves for player 2
            valid_moves = env.getValidMoves()

            # if random float between 0 and 1 is less than epsilon, choose a random action
            if random.random() < epsilon:
                action2 = random.choice(valid_moves)

            # else, choose the action with the highest q-value, but only from the valid moves
            else:
                qvalues = model2.predict(currentState2)
                print("p2 valid moves: ", valid_moves)
                print("p2 qvalues: ", qvalues)

                # remove the q-values for invalid moves by setting invalid moves to negative infinity
                for i in range(7):
                    if i not in valid_moves:
                        qvalues[0][i] = -math.inf

                print("p2 new qvalues: ", qvalues)
                action2 = np.argmax(qvalues[0])
                print("p2 action: ", action2)


            # make the ai player 2 move
            state2, reward_2, gameOver = env.tryMove(action2, 2)

            # check if player 2 won
            if reward_2 >= 10:
                winner = 2
                p2_wins += 1
                reward_1 = -6
                print("p2 wins")
                break

        # if the game is over, but no one won, it's a tie
        if gameOver and winner == None:
            n_ties += 1
            print("tie")
            break

        # Adding new game frame to the next state and deleting the oldest frame from next state
        print("epoch: ", epoch)
        print(f"state: ")
        env.display()
        state1 = np.reshape(state1, (1, env.nRows, env.nColumns, 1))
        state2 = np.reshape(state2, (1, env.nRows, env.nColumns, 1))
        nextState1 = np.append(nextState1, state1, axis = 3)
        nextState1 = np.delete(nextState1, 0, axis = 3)
        nextState2 = np.append(nextState2, state2, axis = 3)
        nextState2 = np.delete(nextState2, 0, axis = 3)
        
        # Remembering the transition and training our AI for player 1
        dqn1.remember([currentState1, action1, reward_1, nextState1], gameOver)
        inputs1, targets1 = dqn1.get_batch(model1, batchSize)
        model1.train_on_batch(inputs1, targets1)

        currentState1 = nextState1

        # Remembering the transition and training our AI for player 2
        dqn2.remember([currentState2, action2, reward_2, nextState2], gameOver)
        inputs2, targets2 = dqn2.get_batch(model2, batchSize)
        model2.train_on_batch(inputs2, targets2)

        currentState2 = nextState2

    
    # Saving the model every 50 epochs
    if epoch % 50 == 0:
        model1.save(filepathToSave1)
        model2.save(filepathToSave2)


    # save a png plotting p1_wins and p2_wins in a dual line graph
    if epoch % 10 == 0:
        print("p1_wins: ", p1_wins)
        print("p2_wins: ", p2_wins)
        print("n_ties: ", n_ties)
        game_history.append([p1_wins, p2_wins, n_ties])
        print("game_history: ", game_history)

        # plot game_history as a triple line graph
        plt.plot(game_history)

        # add colors
        plt.gca().set_prop_cycle(None)
        plt.plot(game_history, color='red')
        plt.plot(game_history, color='blue')
        plt.plot(game_history, color='green')
        
        # add legends
        plt.legend(['p1_wins', 'p2_wins', 'n_ties'])
        plt.xlabel('Sets of 10 games')
        plt.ylabel('Wins per 10 games')
        plt.savefig('test_ims/test3.png')
        plt.clf()


        p1_wins = 0
        p2_wins = 0
        n_ties = 0

    # Lowering the epsilon
    if epsilon > minEpsilon:
        epsilon -= epsilonDecayRate


    # Showing the results each game
    if epoch >= maxEpochs:
        break