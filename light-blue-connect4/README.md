## This project adapts a Deep-Q-Learning model from "the snake game" to play connect 4
![alt text](https://github.com/JonathanBergen/sattler-coursework/blob/f49a0238f7f87536deeac47591bfed98119856fa/light-blue-connect4/test_ims/game.png)
### Added:
- enviroment.py: Added Connect 4 environment with game rules, helper functions, and both PyGame and terminal-based visualiztions
- Image-based real-time model training analysis with matplotlib
### Modified:
- brain.py: changed the network shape and layer system to better learn connect 4, and changed the initial convolutional layer to "see" a 4x4 grid
- train.py: modified the game loop to play connect 4 rather than the snake game
- test.py: modified the visualization and added keyboard support using PyGame 
### How to run
- clone the repo
- optional: train your own model by running train.py with your own learning parameters and model-saving paths
- in test.py, change "filepathToOpen" to your chosen .h5 saved model
- run test.py to play against the model, using the 1-7 keys to place pieces
