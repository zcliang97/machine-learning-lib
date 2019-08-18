import numpy as np
import pandas as pd

class DoubleQLearning:

    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.1):
        self.actions = actions  
        self.alpha = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_tableA = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.q_tableB = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.display_name="Double Q-Learning"

    '''Choose the next action to take given the observed state using an epsilon greedy policy'''
    def choose_action(self, observation):
        self.check_state_exist(observation)
        q_table = self.q_tableA.add(self.q_tableB, fill_value=0)
        action = q_table.loc[observation].idxmax()
        return action

    '''Update the Q(S,A) state-action value table using the latest experience
    '''
    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)

        if s_ != 'terminal':
            # off-policy
            a_ = self.choose_action(str(s_))

            if np.random.random() < 0.5:
                bestA_ = self.q_tableA.loc[s_].idxmax()

                q_delta = r + self.gamma * self.q_tableA.loc[s_, bestA_] - self.q_tableA.loc[s, a]
                q_target = self.q_tableA.loc[s, a] + self.alpha * q_delta
                
                # update Q-table
                self.q_tableA.loc[s, a] = q_target
            else:
                bestA_ = self.q_tableB.loc[s_].idxmax()

                q_delta = r + self.gamma * self.q_tableB.loc[s_, bestA_] - self.q_tableB.loc[s, a]
                q_target = self.q_tableB.loc[s, a] + self.alpha * q_delta
                
                # update Q-table
                self.q_tableB.loc[s, a] = q_target

        else:
            q_target = r  # next state is terminal

            # update Q-table
            self.q_tableA.loc[s, a] = q_target
            self.q_tableB.loc[s, a] = q_target
        return s_, a_


    '''States are dynamically added to the Q(S,A) table as they are encountered'''
    def check_state_exist(self, state):
        if state not in self.q_tableA.index:
            # append new state to q table
            self.q_tableA = self.q_tableA.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_tableA.columns,
                    name=state,
                )
            )
        if state not in self.q_tableB.index:
            # append new state to q table
            self.q_tableB = self.q_tableB.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_tableB.columns,
                    name=state,
                )
            )
