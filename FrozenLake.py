import numpy as np
import gym
# import random
# import time
# from IPython.display import clear_output

env = gym.make("FrozenLake-v1")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))
print(q_table)