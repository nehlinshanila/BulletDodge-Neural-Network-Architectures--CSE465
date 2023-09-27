import gym
import numpy as np
from gym import spaces
import pygame

# obstacle and reward setting
class DotEnv(gym.Env):
    def __init__(self, screen_width=400, screen_height=400):
        super(DotEnv, self).__init__()

        # Define the screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # defining the agent policies
        self.blue_dot_radius = 20
        self.direction_line_length = 20
        self.blue_dot_health = 50
        self.red_dot_health = 50

        # Define action space (left, right, up, down)
        self.action_space = spaces.Discrete(4)

        # Define observation space (positions of blue dot and red dot)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0], dtype=np.float32), high=np.array(
            [self.screen_width / 2, self.screen_height, self.screen_width, self.screen_height], dtype=np.float32),
                                            dtype=np.float32)

        # Initialize the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dots Moving Environment')

        # Initialize the positions of the blue and red dots
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # Define grid line properties
        self.grid_color = (0, 0, 0)
        self.grid_spacing = 20  # Adjust this value to change the grid spacing

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.total_reward = 0

    def reset(self):
        # Reset the positions of the blue and red dots
        self.blue_dot_pos = np.array([0, 0], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.blue_dot_health = 50
        self.total_reward = 0
        return np.concatenate([self.blue_dot_pos, self.red_dot_pos])

    def step(self, action):  #per second 1 frame pass what happens determines step function
        # Define the movement speed
        # self used to access variables
        move_speed = 2.0

        # Separate the action for blue and red dots
        action_blue_dot, action_red_dot = action

        if action_blue_dot == 0:  # Move blue dot left
            self.blue_dot_pos[0] -= move_speed
        elif action_blue_dot == 1:  # Move blue dot right
            self.blue_dot_pos[0] += move_speed
        elif action_blue_dot == 2:  # Move blue dot up
            self.blue_dot_pos[1] -= move_speed
        elif action_blue_dot == 3:  # Move blue dot down
            self.blue_dot_pos[1] += move_speed

        move_speed = 2.03

        # Calculate the direction vector from the red dot to the blue dot
        direction = self.blue_dot_pos - self.red_dot_pos

        # Normalize the direction vector
        direction /= np.linalg.norm(direction)
        print("Direction: ", direction)
        distance_between_centers = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)

        blue_dot_radius = self.blue_dot_radius
        red_dot_radius = blue_dot_radius - 15
        reward = 0
        done = False

        # Check if the dots collide with each other
        if distance_between_centers < blue_dot_radius + red_dot_radius:
            # Separate the dots by moving the red dot away from the blue dot
            self.red_dot_pos -= -50.0 + move_speed * direction
            self.blue_dot_health -= 1
            if(self.blue_dot_health <= 0):
                done = True
            reward = -1
            print("collision")

        else:
            # Move the red dot towards the blue dot with a fixed speed
            self.red_dot_pos += move_speed * direction

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

    def display_total_reward(self):
        text_surface = self.font.render(f"Reward: {self.total_reward: .2f} Blue Health: {self.blue_dot_health}", True, (0, 0, 0))

        text_rect = text_surface.get_rect()

        text_rect.center = (self.screen_width - 200, 10)

        self.screen.blit(text_surface, text_rect)

    def render(self, action_blue, action_red):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw grid lines
        for x in range(0, self.screen_width, self.grid_spacing):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.screen_height), 1)
        for y in range(0, self.screen_height, self.grid_spacing):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y), 1)

        # Draw blue dot
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])), self.blue_dot_radius)

        # Draw red dot
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.red_dot_pos[0]), int(self.red_dot_pos[1])), self.blue_dot_radius - 10)

        # calculating the position of facing direction lines
        blue_dot_direction_end = tuple(map(int, self.blue_dot_pos + self.direction_line_length * action_blue))
        red_dot_direction_end = tuple(map(int, self.red_dot_pos + self.direction_line_length * action_red))

        # direction line draw
        pygame.draw.line(self.screen, (0, 0, 255), tuple(map(int, self.blue_dot_pos)), blue_dot_direction_end, 2)
        pygame.draw.line(self.screen, (255, 0, 0), tuple(map(int, self.red_dot_pos)), red_dot_direction_end, 2)

        self.display_total_reward()

        # Update the display
        pygame.display.update()

    def close(self):
        pygame.quit()


# Example usage of the gym environment
if __name__ == "__main__":
    env = DotEnv()
    # observation = env.reset()
    done = True

    while True:
        # env.render()
        # Control logic for the blue dot (random actions)
        if done:
            observation = env.reset()
            done = False
        action_blue = env.action_space.sample()

        # No action for the red dot (it moves automatically towards the blue dot)
        action_red = env.blue_dot_pos - env.red_dot_pos

        action_red /= np.linalg.norm(action_red)

        action = [action_blue, action_red]

        observation, reward, done, _ = env.step(action)
        env.render(action_blue, action_red)

    env.close()
