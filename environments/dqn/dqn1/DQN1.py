import gym
import numpy as np
import pygame
from gym import spaces

class PredatorPreyEnv(gym.Env):
    def __init__(self, grid_size=5, screen_width=800, screen_height=600):
        super(PredatorPreyEnv, self).__init__()

        self.grid_size = grid_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define the action space (discrete actions: left, right, up, down)
        self.action_space = spaces.Discrete(4)

        # Define observation space (positions of predator and prey)
        self.observation_space = spaces.Box(
            low=np.zeros((self.grid_size, self.grid_size, 2), dtype=np.float32),
            high=np.ones((self.grid_size, self.grid_size, 2), dtype=np.float32),
            dtype=np.float32
        )

        # Initialize the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Predator-Prey Environment')

        # Initialize the positions of predator and prey
        self.predator_position = [0, 0]
        self.prey_position = [self.grid_size - 1, self.grid_size - 1]

        self.max_steps = 100  # Adjust as needed
        self.current_step = 0
        self.total_reward = 0

    def reset(self):
        # Reset positions of predator and prey at the start of each episode
        self.predator_position = [0, 0]
        self.prey_position = [self.grid_size - 1, self.grid_size - 1]

        self.current_step = 0
        self.total_reward = 0

        return self.get_observation()

    def step(self, action):
        predator_velocity = [0, 0]
        prey_velocity = [0, 0]

        # Implement predator's movement logic based on the selected action
        if action == 0:  # Move left
            predator_velocity[0] = -0.1
        elif action == 1:  # Move right
            predator_velocity[0] = 0.1
        elif action == 2:  # Move up
            predator_velocity[1] = -0.1
        elif action == 3:  # Move down
            predator_velocity[1] = 0.1

        # Implement automatic movement logic for prey (random movement)
        prey_velocity = np.random.uniform(-0.1, 0.1, size=(2,))

        # Update predator and prey positions
        self.predator_position = self.move_agent(self.predator_position, predator_velocity)
        self.prey_position = self.move_agent(self.prey_position, prey_velocity)

        # Check for collisions (predator touching prey)
        if self.check_collision():
            # Move the prey away
            self.prey_position = [np.random.randint(self.grid_size), np.random.randint(self.grid_size)]
            # Provide a negative reward for the predator
            reward = -1
        else:
            reward = 0

        # Update the grid to reflect the new positions (if needed)
        # ...

        # Check termination conditions
        done = self.current_step >= self.max_steps

        self.current_step += 1
        self.total_reward += reward

        return self.get_observation(), reward, done, {}

    def move_agent(self, position, velocity):
        # Implement logic to move the agent based on velocity while staying within grid boundaries
        new_position = np.add(position, velocity)
        new_position = np.clip(new_position, [0, 0], [self.grid_size - 1, self.grid_size - 1])
        return new_position

    def check_collision(self):
        # Implement collision detection logic (predator touching prey)
        return np.array_equal(self.predator_position, self.prey_position)

    def get_observation(self):
        # Return the current observation (positions of predator and prey)
        observation = np.zeros((self.grid_size, self.grid_size, 2), dtype=np.float32)
        predator_position = np.array(self.predator_position, dtype=np.int32)
        prey_position = np.array(self.prey_position, dtype=np.int32)

        observation[predator_position[0], predator_position[1], 0] = 1  # Predator's position
        observation[prey_position[0], prey_position[1], 1] = 1  # Prey's position

        return observation

    def render(self, mode='human'):
        if mode == 'human':
            # Clear the screen
            self.screen.fill((255, 255, 255))

            # Draw the grid
            cell_width = self.screen_width // self.grid_size
            cell_height = self.screen_height // self.grid_size

            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.get_observation()[x, y, 0] == 1:
                        pygame.draw.rect(self.screen, (255, 0, 0), (x * cell_width, y * cell_height, cell_width, cell_height))
                    elif self.get_observation()[x, y, 1] == 1:
                        pygame.draw.rect(self.screen, (0, 0, 255), (x * cell_width, y * cell_height, cell_width, cell_height))

            # Update the display
            pygame.display.flip()

        elif mode == 'rgb_array':
            # Render to an RGB array (useful for video recording or further processing)
            frame = pygame.surfarray.array3d(pygame.display.get_surface())
            return frame

    def close(self):
        pygame.quit()

# Example usage
if __name__ == "__main__":
    env = PredatorPreyEnv()
    done = True

    while True:
        if done:
            observation = env.reset()
            done = False
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        env.render()
