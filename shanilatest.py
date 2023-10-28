import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Agent Environment")
import os
import sys
import time
import numpy as np
import pygame
from gymnasium import Env
from gymnasium.spaces import Discrete, Box

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Agents.agent import Agent
from Agents.RayCast import get_fov_rays
from Constants.constants import WHITE, RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, WALLS, LEVEL_3_WALLS
from Walls.collision_detection import detect_collision
from Walls.wall_class import Walls



class GameEnv(Env):
    def __init__(self, render_mode='human'):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.render_mode = render_mode

        total_values = 219
        self.observation_space = Box(
            low=np.zeros(total_values, dtype=np.float32),
            high=self.screen_width * np.ones(total_values, dtype=np.float32),
            dtype=np.float32
        )

        # Define the radius for the semi-circular reward area
        self.semi_circle_radius = 250  # You can adjust this radius

        #! Define the center of the screen for the green dot
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2

        self.action_space = Discrete(5)

        self.total_steps = 0

        self.number_of_predator = 1

        self.predator_agent = None

        self.predator_total_reward = 0

        self.obs = None

        # start the tick timer
        self.start_time = 0
        self.total_running_time = 10

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Multi Agent Environment(simple)')

        pygame.font.init()
        self.font = pygame.font.Font(None, 18)

        self.wall = Walls(pygame)
        self.walls = None

    def agent_init(self):
        predator_agents = Agent('predator', 0)
        self.predator_agent = predator_agents

    def flatten_list(self, nested_list):
        flattened_list = []
        for item in nested_list:
            if isinstance(item, list):
                flattened_list.extend(self.flatten_list(item))
            else:
                flattened_list.append(item)
        return flattened_list
    
    def _get_obs(self):
        observation = []
        agent_pos = [self.predator_agent.current_position[0], self.predator_agent.current_position[1]]
        observation.append(agent_pos)

        angle = self.predator_agent.angle
        observation.append(angle)

        value_list = get_fov_rays(agent_pos)
        observation.append(value_list)
        
        observation = self.flatten_list(observation)
        return observation

    def _max_right(self):
        max_right = 0
        for wall in self.walls:
            if wall.right > max_right:
                max_right = wall.right
        return max_right

    def reset(self, seed=0):
        self.start_time = time.time()
        self.agent_init()
        self.wall.clear_walls()
        self.walls = self.wall.make_wall(LEVEL_3_WALLS)
        self.total_steps = 0
        self.predator_total_reward = 0

        predator = self.predator_agent
        predator.agent_reset(width=self.screen_width, height=self.screen_height, walls=self.walls)

        self.predator_agent = predator

        observation = self._get_obs()
        self.obs = observation

        return observation, seed

    def step(self, action):
        done = False
        reward = 0
        truncated = False
        info = {}
        current_time = time.time()

        elapsed_time = current_time - self.start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
        self.predator_agent.step_update(action, range_x=self.screen_width, range_y=self.screen_height)
        self.predator_agent = detect_collision(self.predator_agent, self.walls)

        # Calculate the center of the exponential reward area
        center_x, center_y = 325, 300
        # Calculate the distance from the agent to the center
        distance_to_center = ((self.predator_agent.current_position[0] - center_x) ** 2 + (self.predator_agent.current_position[1] - center_y) ** 2) ** 0.5
        # Set the radius for the exponential reward function to start working
        radius_for_exponential_reward = 250  # Adjust this radius as needed
        # Check if the agent is within the exponential reward area
        if distance_to_center <= radius_for_exponential_reward:
            reward = 10 * np.exp(-1 * distance_to_center / 100) + 0.05

        if self.predator_agent.current_position[0] > self._max_right():
            reward += 100
            done = True

        if elapsed_time >= self.total_running_time:
            reward -= 50
            done = True

        # reward += 0.01
        self.render()

        observation = self._get_obs()
        self.predator_total_reward = reward
        self.obs = observation

        return observation, reward, done, truncated, info

    def render(self):
        if self.render_mode == 'human':
            screen = self.screen
            screen.fill(WHITE)
            
            predator = self.predator_agent
            pygame.draw.circle(screen, RED, predator.center, predator.radius)
            pygame.draw.line(screen, RED, predator.center, predator.draw_direction_end, 5)

            for key, wall in LEVEL_3_WALLS.items():
                pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))


            # Calculate the center of the exponential reward area
            center_x, center_y = 325, 300
            # Calculate the distance from the agent to the center
            distance_to_center = ((self.predator_agent.current_position[0] - center_x) ** 2 + (self.predator_agent.current_position[1] - center_y) ** 2) ** 0.5
            # Check if the agent is within the exponential reward area
            if distance_to_center <= 250:  # Adjust this radius as needed
                reward = 100 * np.exp(-2 * distance_to_center / 100) - 1.5


            max_right = self._max_right()
            pygame.draw.circle(screen, (0, 255, 0), (325, 300), 5)

            max_right_color = (255, 0, 0)
            pygame.draw.line(self.screen, max_right_color, (max_right, 0), (max_right, self.screen_height), 2)

            pygame.display.update()

    def close(self):
        pygame.quit()

def main():
    # Initialize the environment
    env = GameEnv(render_mode='human')

    # Reset the environment to get the initial observation
    observation, seed = env.reset()

    done = False
    while not done:
        # Replace this with your agent's logic to choose actions
        # In this example, we're taking a random action.
        action = env.action_space.sample()

        # Step through the environment with the chosen action
        observation, reward, done, truncated, info = env.step(action)

    # Close the environment when done
    env.close()

if __name__ == "__main__":
    main()

# Define colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Define green color

# Predator agent position and size
predator_x, predator_y = WIDTH // 2, HEIGHT // 2
predator_radius = 10  # Radius of the circular predator agent
move_step = 0.1  # Adjust the movement step

# Define walls in a dictionary
walls = {
    # "wall1": {"x": 100, "y": 100, "width": 20, "height": 100},
    "wall2": {"x": 200, "y": 300, "width": 20, "height": 100},
    "wall3": {"x": 300, "y": 200, "width": 20, "height": 100},
}

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        predator_x -= move_step
    if keys[pygame.K_RIGHT]:
        predator_x += move_step
    if keys[pygame.K_UP]:
        predator_y -= move_step
    if keys[pygame.K_DOWN]:
        predator_y += move_step

    # Clear the screen
    screen.fill(WHITE)

    # Draw the predator agent as a circle
    pygame.draw.circle(screen, RED, (predator_x, predator_y), predator_radius)

    # Draw walls from the dictionary with green color
    for wall in walls.values():
        pygame.draw.rect(screen, GREEN, (wall["x"], wall["y"], wall["width"], wall["height"]))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
