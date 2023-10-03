import numpy as np
import gym
import random
import time
from IPython.display import clear_output

env = gym.make("FrozenLake-v1")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))
# print(q_table)

# create and initialize all the parameters needed for q-learning
num_episodes = 10000  # total num of episodes we want agent to play
max_steps_per_episode = 100  # max number of step agent is allowed to take in 1 episode

learning_rate = 0.1  # alpha
discount_rate = 0.99  # gamma
# exploration and exploitation tradeoff
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

rewards_all_episodes = []
# Q-Learning Algorithm
for episode in range(num_episodes):
    state = env.reset()

    done = False  # if or if not episode is finished
    rewards_current_episode = 0  # start out with no rewards

    for step in range(max_steps_per_episode):

        # Exploration Exploitation tradeoff
        exploration_rate_threshold = random.uniform(0, 1)  # whether agent will explore or exploit
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state, :])
            # agent will exploit using the highest q value in q table
        else:
            action = env.action_space.sample()
            # agent will explore and sample an action randomly

        new_state, reward, done, truncated, info = env.step(action)
        # print(env.step(action))

        # Update qtable for Q(s, a) using the formula below
        state = int(state)
        action = int(action)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
                                 learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

        state = new_state
        rewards_current_episode += reward

        if done == True:
            break

    # Exploration rate decay which decays as proportional to current value
    exploration_rate = min_exploration_rate + \
                       (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)

# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes / 1000)
count = 1000
print("*********Average reward per thousand episodes******\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r / 1000)))
    count += 1000

# print updated Q-table
print("\n\n******Q-table******\n")
print(q_table)
