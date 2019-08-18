from ReinforcementLearning import ReinforcementLearning
actions = [1,2,3]
def rewards(state, nextState):
    return 1
def move(state, action):
    return 1
rl = ReinforcementLearning('qlearning', actions, rewards, move)
