# Reinforcement Learning

A collection of common RL learning techniques with commonly used models.

## Included Models

- Q-Learning
- SARSA
- Double Q-Learning
- Expected SARSA

## Setup

To use the models, must create an environment file with the following parameters.

- __Actions list__: `action list = list(range(possible_moves))`

... All actions must be mapped to a range of indexes. The range of indexes will be passed into the model as a list of integers.

- __Reward function__: `def reward(currState, nextState)`

... A function that computes the reward for moving from one state to another state.

- __Move function__: `def move(currState, action)`

... A function that returns the next state given the current state and a decided action.

- __Number of Episodes (Epoch)__: `default [1000]`

... The number of episodes/epoches that the algorithm will run through.

- __Epsilon-Greedy__: `default [0.1]`

... The greedy parameter used when making a move. Will choose a greedy move `1-\(\epsilon\)` of the time and a random move `\(\epsilon\)` of the time.

- __Learning rate (alpha)__: `default [0.2]`

... The rate at which information (state/action -> reward) is updated into the Q-table and learned.

- __Reward Decay (gamma)__: `default [0.9]`

... The decay of which future rewards are weighted. High values correspond to a more _farsighted_ model and low values correspond to a more _nearsighted_ model.