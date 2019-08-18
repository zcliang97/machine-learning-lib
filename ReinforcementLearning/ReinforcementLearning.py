import numpy as np

from models.sarsa import SARSA
from models.qlearning import QLearning
from models.expected_sarsa import ExpectedSARSA
from models.double_qlearning import DoubleQLearning

class ReinforcementLearning:
    def __init__(self, model, actions, rewardFunction, moveFunction, episodes=1000, epsilon_greedy=0.1, learning_rate=0.2, reward_decay=0.9):
        # set parameters
        self.numEpisodes = episodes
        self.epsilon = epsilon_greedy
        self.alpha = learning_rate
        self.gamma = reward_decay
        self.actions = actions
        self.rewards = rewardFunction
        self.move = moveFunction

        # init model
        if model == 'qlearning':
            self.model = QLearning(actions, learning_rate, reward_decay, epsilon_greedy)
        elif model == 'sarsa':
            self.model = SARSA(actions, learning_rate, reward_decay, epsilon_greedy)
        elif model == 'esarsa':
            self.model = ExpectedSARSA(actions, learning_rate, reward_decay, epsilon_greedy)
        elif model == 'dblqlearing':
            self.model = DoubleQLearning(actions, learning_rate, reward_decay, epsilon_greedy)
    
    def run(self, start_state):
        state = start_state
        global_reward = np.zeros(self.numEpisodes)

        # iterate through the episodes
        for ep in range(self.numEpisodes):
            # choose action based on state
            action = self.model.choose_action(str(state))
            while True:
                # RL take action and get next state and reward
                state_, reward, done = self.step(str(state), action)
                global_reward[ep] += reward

                # RL learn from this transition and determine next state and action
                state, action = self.model.learn(str(state), action, reward, str(state_))
    
                # break while loop when end of this episode
                if done:
                    break

        return global_reward
        
    def step(self, state, action):
        # get the next state by doing the action from the state
        nextState = self.move(state, action)

        # call the reward function
        reward, done = self.rewards(state, nextState)

        return nextState, reward, done