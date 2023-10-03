import gym
import numpy as np
import pygame
import time

# Create a custom Gym environment for the predator-prey scenario
class PredatorPreyEnv(gym.Env):
    def __init__(self):
        super(PredatorPreyEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(4)  # Four discrete actions: up, down, left, right
        self.observation_space = gym.spaces.Discrete(4)  # Four discrete states for simplicity
        self.prey_position = None
        self.predator_position = None
        self.reset()

    def reset(self):
        self.prey_position = np.random.randint(0, 4)  # Initialize prey position randomly
        self.predator_position = np.random.randint(0, 4)  # Initialize predator position randomly
        return self.prey_position

    def step(self, prey_action, predator_action):
        # Update prey's position based on its action
        self.prey_position = (self.prey_position + prey_action) % 4

        # Update predator's position based on its action
        self.predator_position = (self.predator_position + predator_action) % 4

        # Define the reward structure
        if self.prey_position == self.predator_position:
            # Predator catches prey
            reward_prey = -10
            reward_predator = 10
            done = True
        else:
            reward_prey = 1
            reward_predator = -1
            done = False

        return self.prey_position, reward_prey, reward_predator, done, {}

# Instantiate the environment
env = PredatorPreyEnv()

# Q-learning parameters
num_episodes = 1000
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

# Q-tables for prey and predator
prey_q_table = np.zeros((4, 4))
predator_q_table = np.zeros((4, 4))

# Q-learning algorithm
for episode in range(num_episodes):
    state = env.reset()
    done = False
    while not done:
        # Choose actions for prey and predator (using epsilon-greedy policy)
        if np.random.uniform(0, 1) < epsilon:
            prey_action = env.action_space.sample()  # Explore
            predator_action = env.action_space.sample()  # Explore
        else:
            prey_action = np.argmax(prey_q_table[state, :])  # Exploit
            predator_action = np.argmax(predator_q_table[state, :])  # Exploit

        # Take actions and receive rewards
        new_state, reward_prey, reward_predator, done, _ = env.step(prey_action, predator_action)

        # Update Q-tables for prey and predator
        prey_q_table[state, prey_action] = (1 - learning_rate) * prey_q_table[state, prey_action] + \
                                            learning_rate * (reward_prey + discount_factor * np.max(prey_q_table[new_state, :]))

        predator_q_table[state, predator_action] = (1 - learning_rate) * predator_q_table[state, predator_action] + \
                                                    learning_rate * (reward_predator + discount_factor * np.max(predator_q_table[new_state, :]))

        state = new_state

# Initialize Pygame for visualization
pygame.init()
screen_size = 400
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Predator-Prey Environment")

# Define colors
GREY = (217, 217, 217)
RED = (105, 109, 125)
GREEN = (242, 162, 202)

# Function to draw the environment
def draw_environment(prey_position, predator_position):
    screen.fill(GREY)
    cell_size = screen_size // 4
    pygame.draw.rect(screen, GREEN, (prey_position * cell_size, 0, cell_size, cell_size))
    pygame.draw.rect(screen, RED, (predator_position * cell_size, 3 * cell_size, cell_size, cell_size))
    pygame.display.flip()


# Testing the learned policies
state = env.reset()
done = False
while not done:
    prey_action = np.argmax(prey_q_table[state, :])
    predator_action = np.argmax(predator_q_table[state, :])
    new_state, _, _, done, _ = env.step(prey_action, predator_action)
    state = new_state

    # Update the visualization
    draw_environment(state, env.predator_position)
    time.sleep(0.5)  # Add a small delay to see the animation

print("Simulation complete.")
