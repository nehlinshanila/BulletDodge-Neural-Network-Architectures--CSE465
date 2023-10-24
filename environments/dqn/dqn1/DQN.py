import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame

class PredatorPreyENV(gym.Env):
    # The primary purpose of PredatorPreyENV is to store configuration settings and sensitive information
    #  Python class named PredatorPreyENV that inherits from the custom gym.Env
    def __init__(self, screen_width=800, screen_height=600):
        super(PredatorPreyENV, self).__init__()

        # Define the screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # defining the agent policies
        self.blue_dot_radius = 40
        self.direction_line_length = 40
        self.blue_dot_health = 50
        self.red_dot_health = 50
        
        # Define the attack damage of the red dot
        self.red_dot_attack_dmg = 10  # Adjust this value as needed
        
        # Define movement speeds for blue and red dots
        self.blue_dot_move_speed = 0.8
        self.red_dot_move_speed = 0.5

        # Define 4 discreet action space (left, right, up, down)
        self.action_space = spaces.Discrete(4)

        # Define observation space (positions of blue dot and red dot)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0], dtype=np.float32), high=np.array(
            [self.screen_width / 2, self.screen_height, self.screen_width, self.screen_height], dtype=np.float32),
                                            dtype=np.float32)

        # Initialize the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Predator-Prey Environment')

        # Initialize the positions of the blue and red dots
        # self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # Define grid line properties
        self.grid_color = (210, 210, 210)
        self.grid_spacing = 40  # Adjust this value to change the grid spacing

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.total_reward = 0
    #     keep track of the cumulative reward earned by the agent as it interacts with the environment
    # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Predator-Prey Environment')


    def reset(self, seed=0):
        super().reset(seed=seed)
        # Reset the positions of the blue and red dots at start of each episodes
        # self.blue_dot_pos = np.array([0, 0], dtype=np.float32)
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # Reset the position of the red dot to the middle of the screen
        # self.red_dot_pos = np.array([self.screen_width / 2, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        self.blue_dot_health = 50
        self.total_reward = 0
        return np.concatenate([self.blue_dot_pos, self.red_dot_pos]), seed 

    # This function essentially describes how the blue and red dots interact
    # based on the selected actions, handle collisions, and update their positions and rewards within the environment.
    def step(self, action_blue_dot):  #per second 1 frame pass what happens determines step function
        # truncated == false
        # Define the movement speed
        # self used to access variables
        move_speed_blue = 0.8   #blue
        move_speed_red = 0.1   # red

        action_red_dot = 0

        # Separate the action for blue and red dots
        # action_blue_dot, action_red_dot = action
        # POLICIES
        if action_blue_dot == 0:  # Move blue dot left
            self.blue_dot_pos[0] -= move_speed_blue
        elif action_blue_dot == 1:  # Move blue dot right
            self.blue_dot_pos[0] += move_speed_blue
        elif action_blue_dot == 2:  # Move blue dot up
            self.blue_dot_pos[1] -= move_speed_blue
        elif action_blue_dot == 3:  # Move blue dot down
            self.blue_dot_pos[1] += move_speed_blue


        # Calculate the direction vector from the red dot to the blue dot by subtracting
        direction = self.blue_dot_pos - self.red_dot_pos

        # Normalize the direction vector by dividing the vector by its magnitude (length) to turn it into a unit vector
        direction /= np.linalg.norm(direction)
        # normalized vector (direction) indicates the direction from the red dot to the blue dot.
        print("Direction: ", direction)
        distance_between_centers = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)
        # calculates the Euclidean distance between the centers of the blue and red dots,
        # measures how far apart the two dots are in terms of pixel distance.

        # radii for collision detection. The red_dot_radius is set to be 15 pixels smaller than the blue_dot_radius.
        blue_dot_radius = self.blue_dot_radius
        red_dot_radius = blue_dot_radius - 15
        reward = 0
        done = False

        # Check if the dots collide with each other
        # checking if the distance between the centers of the blue and red dots (distance_between_centers)
        # is less than the sum of their radii (blue_dot_radius + red_dot_radius)
        if distance_between_centers < blue_dot_radius + red_dot_radius:
            # Separate the dots by moving the red dot away from the blue dot
            self.red_dot_pos -= -50.0 + move_speed_red * direction
            self.blue_dot_health -= self.red_dot_attack_dmg
            if(self.blue_dot_health <= 0):
                done = True
            reward -= 5
            print("collision")

        else:
            # Move the red dot towards the blue dot with a fixed speed
            self.red_dot_pos += move_speed_red * 100 * direction

        # Clip blue dot position to stay within the first half of the screen
        self.blue_dot_pos[0] = np.clip(self.blue_dot_pos[0], 0, self.screen_width)
        self.blue_dot_pos[1] = np.clip(self.blue_dot_pos[1], 0, self.screen_height)

        # Clip red dot position to stay within the entire screen
        self.red_dot_pos = np.clip(self.red_dot_pos, [0, 0], [self.screen_width, self.screen_height])

        # Define a simple reward function (e.g., distance between the two dots)
        # reward = -np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)
        self.total_reward += reward

        # Check if the dots are close to each other (you can adjust the distance threshold as needed)
        # done = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos) < 10
        return np.concatenate([self.blue_dot_pos, self.red_dot_pos]), reward, done, {}
    # done flag indicating the end of the episode, and an empty dictionary ({}) for additional information

    def display_total_reward(self):
        text_surface = self.font.render(f"Reward: {self.total_reward: .2f} Blue Health: {self.blue_dot_health}", True, (0, 0, 0))
        # the reward and blue dot health values text
        text_rect = text_surface.get_rect()
        # position the text on the pygame window.
        text_rect.center = (self.screen_width - 200, 10)
        self.screen.blit(text_surface, text_rect)
    # The blit method is used to draw the text surface (text_surface) onto the pygame window (self.screen)

    # render function is responsible for creating a visual representation of the environment
    def render(self, mode='human', action_blue=None, action_red=None):
        if mode == 'human':
            # Clear the screen
            self.screen.fill((229, 222, 248))

            # Draw grid lines
            for x in range(0, self.screen_width, self.grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.screen_height), 1)
            for y in range(0, self.screen_height, self.grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y), 1)

            # Draw blue dot
            pygame.draw.circle(self.screen, (141,144,226), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])), self.blue_dot_radius)

            # Draw red dot
            pygame.draw.circle(self.screen, (158, 50, 90), (int(self.red_dot_pos[0]), int(self.red_dot_pos[1])), self.blue_dot_radius - 10)

            # calculating the position of facing direction lines
            if action_blue is not None:
                blue_dot_direction_end = tuple(map(int, self.blue_dot_pos + self.direction_line_length * action_blue))
                pygame.draw.line(self.screen, (0, 0, 255), tuple(map(int, self.blue_dot_pos)), blue_dot_direction_end, 2)

            if action_red is not None:
                red_dot_direction_end = tuple(map(int, self.red_dot_pos + self.direction_line_length * action_red))
                pygame.draw.line(self.screen, (255, 0, 0), tuple(map(int, self.red_dot_pos)), red_dot_direction_end, 2)

            self.display_total_reward()

            # Update the display
            pygame.display.update()
        elif mode == 'rgb_array':
            pass

    def close(self):
        pygame.quit()

# Main loop
env = PredatorPreyENV()  # Create an instance of the environment
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perform environment steps and rendering
    action_blue = env.action_space.sample()  # Replace with your agent's action selection logic
    _, _, done, _ = env.step(action_blue)

    # Render the environment with the 'human' mode
    env.render(mode='human', action_blue=action_blue, action_red=None)  # Pass the mode and action parameters

    # Optionally, control the frame rate
    pygame.time.delay(50)  # Adjust the delay as needed

    if done:
        env.reset()

# Close the environment and Pygame window
env.close()