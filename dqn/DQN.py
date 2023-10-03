import gymnasium as gym
from gym import spaces
import pygame
import numpy as np

# stables baselines3 function
class PredatorPreyEnv:
    def __init__(self, grid_size=5):
        # Initialize Pygame window and other environment attributes here
        pygame.init()
        self.screen_width = 400
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Predator-Prey Environment')

        self.grid_size = grid_size  # Added grid_size as a parameter

        # Define continuous action spaces for predator and prey
        self.action_space_predator = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self.action_space_prey = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        # Use dtype=np.float32 for the observation space
        self.observation_space = spaces.Box(low=np.zeros((self.grid_size, self.grid_size), dtype=np.float32),
                                            high=np.ones((self.grid_size, self.grid_size), dtype=np.float32),
                                            dtype=np.float32)

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.predator_position = [0.5, 0.5]  # Corrected variable name
        self.prey_position = [self.grid_size - 0.5, self.grid_size - 0.5]  # Corrected variable name
        self.obstacle_pos = [[2, 2], [3, 3]]

        self.max_steps = 20
        self.current_step = 0

    def reset(self):
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int)
        initial_position = [self.grid_size // 2, self.grid_size // 2]  # Middle of the grid
        self.predator_position = initial_position
        self.prey_position = initial_position
        self.obstacle_pos = [[2, 2], [3, 3]]  # You can adjust obstacle positions if needed
        self.current_step = 0
        self.place_objects()
        return self.grid.copy()

    def step(self, actions):
        # Calculate the distance between the predator and prey
        distance = np.linalg.norm(np.array(self.predator_position) - np.array(self.prey_position))

        if distance < 0.1:  # You can adjust this distance threshold as needed
            # If the predator is very close to the prey, move the prey away
            prey_speed = 0.03  # Adjust the speed as needed
            random_movement = np.random.uniform(-1, 1, size=(2,))
            random_movement /= np.linalg.norm(random_movement)
            new_prey_position = np.array(self.prey_position) + random_movement * prey_speed
            new_prey_position = np.clip(new_prey_position, [0, 0], [self.grid_size - 1, self.grid_size - 1])
            self.prey_position = new_prey_position.tolist()

        # Calculate the direction from the predator to the prey
        direction = np.array(self.prey_position) - np.array(self.predator_position)

        # Normalize the direction vector to have unit length
        direction /= np.linalg.norm(direction)

        # Calculate the new position of the predator by moving it towards the prey
        predator_speed = 0.05  # Adjust the speed as needed
        new_predator_position = np.array(self.predator_position) + direction * predator_speed

        # Ensure the new position stays within the grid boundaries
        new_predator_position = np.clip(new_predator_position, [0, 0], [self.grid_size - 1, self.grid_size - 1])

        # Update the predator's position
        self.predator_position = new_predator_position.tolist()

        # Check for collisions with obstacles and boundaries (you can keep your collision logic here)

        # Update the grid to reflect the new positions

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.place_objects()

        # Calculate rewards and check termination conditions
        reward = self.calculate_reward()
        done = self.current_step >= self.max_steps
        self.current_step += 1

        return self.grid.copy(), reward, done, {}

    def render(self, mode='human'):
        if mode == 'human':
            # Clear the screen
            self.screen.fill((255, 255, 255))

            # Draw the grid
            cell_size = self.screen_width // self.grid_size
            for x in range(0, self.screen_width, cell_size):
                pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, cell_size):
                pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.screen_width, y))

            # Draw predator and prey as circles
            predator_color = (255, 0, 0)
            prey_color = (0, 0, 255)

            predator_x, predator_y = self.predator_position
            prey_x, prey_y = self.prey_position

            # Draw predator as a circle
            predator_radius = cell_size // 4  # Smaller radius
            pygame.draw.circle(self.screen, predator_color,
                               (int(predator_x * cell_size + cell_size // 2),
                                int(predator_y * cell_size + cell_size // 2)),
                               predator_radius)

            # Draw prey as a circle
            prey_radius = cell_size // 4  # Smaller radius
            pygame.draw.circle(self.screen, prey_color,
                               (int(prey_x * cell_size + cell_size // 2), int(prey_y * cell_size + cell_size // 2)),
                               prey_radius)

            # Update the display
            pygame.display.flip()

        elif mode == 'rgb_array':
            # Render to an RGB array (useful for video recording or further processing)
            # Create a copy of the screen surface as a NumPy array
            frame = pygame.surfarray.array3d(pygame.display.get_surface())
            return frame

        elif mode == 'ansi':
            # Return a text-based representation (not applicable for Pygame)
            pass

    def close(self):
        pygame.quit()

    def place_objects(self):
        # Clear the grid
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)

        # Place predator randomly on the grid
        predator_x = np.random.uniform(0, self.grid_size)
        predator_y = np.random.uniform(0, self.grid_size)
        self.predator_position = [predator_x, predator_y]
        self.grid[int(predator_y)][int(predator_x)] = 1  # Use a unique value for the predator

        # Place prey randomly on the grid (initially far from the predator)
        prey_x = np.random.uniform(0, self.grid_size)
        prey_y = np.random.uniform(0, self.grid_size)
        while np.linalg.norm(np.array([prey_x, prey_y]) - np.array([predator_x, predator_y])) < 2:
            prey_x = np.random.uniform(0, self.grid_size)
            prey_y = np.random.uniform(0, self.grid_size)
        self.prey_position = [prey_x, prey_y]
        self.grid[int(prey_y)][int(prey_x)] = 2  # Use a unique value for the prey

        # Place obstacles on the grid (if needed)
        for obstacle_x, obstacle_y in self.obstacle_pos:
            self.grid[obstacle_y][obstacle_x] = 3  # Use a unique value for obstacles

    def move_agent(self, agent_position, velocity):
        # Calculate the new position based on the velocity
        new_x = agent_position[0] + velocity[0]
        new_y = agent_position[1] + velocity[1]

        # Ensure the new position stays within the grid boundaries
        new_x = np.clip(new_x, 0, self.grid_size - 1)
        new_y = np.clip(new_y, 0, self.grid_size - 1)

        # Return the new position
        return [new_x, new_y]

    def check_collisions(self):
        # Check for collisions between the predator and obstacles
        for obstacle_x, obstacle_y in self.obstacle_pos:
            if np.array_equal(self.predator_position, [obstacle_x, obstacle_y]):
                # Handle collision between predator and obstacle (e.g., reset predator position)
                self.predator_position = [0.5, 0.5]  # Reset predator position to the center

        # Check for collisions between the prey and obstacles (if needed)
        # You can implement this part if your prey should avoid obstacles

        # Check for collisions between the predator and the prey
        if np.array_equal(self.predator_position, self.prey_position):
            # Handle collision between predator and prey (e.g., reset prey position)
            self.prey_position = [self.grid_size - 0.5, self.grid_size - 0.5]  # Reset prey position

        # You can add more collision checks as needed

    def calculate_reward(self):
        # Define your reward logic here
        # Example: Reward the predator for catching the prey and penalize collisions with obstacles

        reward = 0  # Initialize the reward

        # Check if the predator has caught the prey
        if np.array_equal(self.predator_position, self.prey_position):
            reward += 1  # Reward for catching the prey

        # Optionally, you can penalize the predator for colliding with obstacles
        for obstacle_x, obstacle_y in self.obstacle_pos:
            if np.array_equal(self.predator_position, [obstacle_x, obstacle_y]):
                reward -= 0.1  # Penalize for colliding with an obstacle

        return reward


if __name__ == "__main__":
    env = PredatorPreyEnv(grid_size=5)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Your game logic here
        actions = [0.1, 0.1]  # Replace with actual actions
        obs, reward, done, _ = env.step(actions)

        env.render()

        # Add a delay to control the frame rate (e.g., 60 frames per second)
        pygame.time.delay(100)  # Delay for approximately 16 milliseconds (1000 ms / 60 FPS)

    pygame.quit()
