import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame
import random

# reset and step function
class DotEnv(gym.Env):
    def __init__(self, screen_width=700, screen_height=700, render_mode='human'):
        super(DotEnv, self).__init__()

        # screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        # defining the agent policies
        self.direction_line_length = 20
        self.game_speed = 1
        self.test_health = 50


        # for Blue dot
        self.blue_dot_radius = 30
        self.blue_dot_health = 50
        self.blue_dot_attack_dmg = 1
        self.blue_dot_search_radius = 100
        self.blue_dot_turn_rate = None
        self.blue_dot_stamina = 50
        self.blue_dot_stamina_recovery_rate = 15
        self.blue_dot_pos_prev = None

        # for Red dot
        self.red_dot_radius = self.blue_dot_radius - 10
        self.red_dot_health = 50
        self.red_dot_attack_dmg = 1
        self.red_dot_search_radius = None
        self.red_dot_turn_rate = None

        # for Pink food
        self.food_radius = 20
        self.food_position = np.array([self.screen_width / 2, self.screen_height / 2], dtype=np.float32)

        # Reward values
        self.food_reward = 100  # Reward for collecting food
        self.collision_penalty = -20  # Penalty for colliding with the red dot

        # action space (left, right, up, down) for both
        self.action_space = spaces.Discrete(4)

        # Define observation space (positions of blue dot and red dot)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0], dtype=np.float32),
                                            high=np.array([self.screen_width / 2, self.screen_height, self.screen_width, self.screen_height], dtype=np.float32),
                                            dtype=np.float32)

        # Initializing the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dots Moving Environment')

        # Initializing the positions of the blue and red dots
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # # Define grid line properties
        # self.grid_color = (210, 210, 210)
        # self.grid_spacing = 40  # Adjust this value to change the grid spacing

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        # defining the reward for the agent
        self.total_reward = 0

        self.obstacles = [
            (200, 100, 20, 150),
            (300, 250, 50, 20)
        ]

    def reset(self, seed=0):
        super().reset(seed=seed)

        # Reset the positions of the blue and red dots
        self.blue_dot_pos = np.array([self.screen_width / 2, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        self.blue_dot_health = self.test_health
        self.total_reward = 0

        # Reset the position of the pink food to a random location inside the circular area
        while True:
            food_x = random.uniform(0, self.screen_width)
            food_y = random.uniform(0, self.screen_height)
            if np.linalg.norm(np.array([food_x, food_y]) - np.array(
                    [self.screen_width / 2, self.screen_height / 2])) <= self.screen_width / 2:
                break
        self.food_position = np.array([food_x, food_y], dtype=np.float32)

        # Return the initial observation (concatenate blue dot position and red dot position)
        observation = np.concatenate([self.blue_dot_pos, self.red_dot_pos])
        # print(observation)

        return [observation, seed]

    def step(self, step_action):
        reward = 0
        step_done = False

        # Define the movement speed for blue and red dots
        blue_move_speed = 0.9 * self.game_speed
        red_move_speed = 0.1 * self.game_speed

        # Store the previous position of the blue dot
        prev_blue_dot_pos = np.copy(self.blue_dot_pos)

        # unpacking the action for blue and red dots
        action_blue_dot = step_action

        # Move blue dot
        if action_blue_dot == 0:  # Move blue dot left
            self.blue_dot_pos[0] -= blue_move_speed
        elif action_blue_dot == 1:  # Move blue dot right
            self.blue_dot_pos[0] += blue_move_speed
        elif action_blue_dot == 2:  # Move blue dot up
            self.blue_dot_pos[1] -= blue_move_speed
        elif action_blue_dot == 3:  # Move blue dot down
            self.blue_dot_pos[1] += blue_move_speed

        # Calculate the distance between the blue dot and the center of the circle
        distance_to_center = np.linalg.norm(
            self.blue_dot_pos - np.array([int(self.screen_width / 2), int(self.screen_height / 2)]))

        # Check if the blue dot collides with the edge of the circle
        if distance_to_center > int(self.screen_width / 2):
            # Reflect the blue dot off the edge of the circle
            self.blue_dot_pos = self.blue_dot_pos - 2 * (
                    self.blue_dot_pos - np.array([int(self.screen_width / 2), int(self.screen_height / 2)]))

        # Calculate the direction vector from the red dot to the blue dot
        direction = self.blue_dot_pos - self.red_dot_pos

        # Normalize the direction vector
        direction /= np.linalg.norm(direction)

        distance_between_centers = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)

        # Move red dot
        self.red_dot_pos += red_move_speed * direction

        # Clip blue dot position to stay within the first half of the screen
        self.blue_dot_pos[0] = np.clip(self.blue_dot_pos[0], 0, self.screen_width / 2)
        self.blue_dot_pos[1] = np.clip(self.blue_dot_pos[1], 0, self.screen_height)

        # Clip red dot position to stay within the entire screen
        self.red_dot_pos = np.clip(self.red_dot_pos, [0, 0], [self.screen_width, self.screen_height])

        # Calculate the distance between the blue dot and the food
        distance_to_food = np.linalg.norm(self.blue_dot_pos - self.food_position)

        # Check if the blue dot has collected the food
        if distance_to_food < self.blue_dot_radius + self.food_radius:
            # Blue dot collected the food, increase the reward
            reward += self.food_reward

            # Respawn the food to a random location within the circular boundary
            while True:
                new_food_position = np.array(
                    [random.uniform(0, self.screen_width), random.uniform(0, self.screen_height)],
                    dtype=np.float32)
                if np.linalg.norm(new_food_position - np.array([self.screen_width / 2, self.screen_height / 2])) < int(
                        self.screen_width / 2) - self.food_radius:
                    self.food_position = new_food_position
                    break

        # Check if the dots collide with each other
        if distance_between_centers < self.blue_dot_radius + self.red_dot_radius:
            # Separate the dots by moving the red dot away from the blue dot
            self.red_dot_pos -= -50.0 + red_move_speed * direction
            self.blue_dot_health -= self.red_dot_attack_dmg

            if self.blue_dot_health == 0:
                step_done = True
            # print("collision")
            reward += self.collision_penalty  # Update the collision penalty

        if self.blue_dot_health >= 7:
            reward += 0.01

        if self.blue_dot_health == 0:
            reward -= 100

        # Update the total_reward, which includes food_reward and collision_penalty
        self.total_reward += reward

        step_observation = np.concatenate([self.blue_dot_pos, self.red_dot_pos])

        return step_observation, reward, step_done, False, {}

    def display_total_reward(self):
        text_surface = self.font.render(f"Reward: {self.total_reward: .2f} Blue Health: {self.blue_dot_health}", True, (0, 0, 0))

        text_rect = text_surface.get_rect()

        text_rect.center = (self.screen_width - 200, 10)

        self.screen.blit(text_surface, text_rect)

    def render(self):
        if self.render_mode == 'human':
            # Clear the screen
            self.screen.fill((93, 97, 140))

            # Fill the entire space inside the circle with a different color (e.g., green)
            pygame.draw.circle(self.screen, (234, 222, 255), (int(self.screen_width / 2), int(self.screen_height / 2)),
                               int(self.screen_width / 2) - 1)

            # Draw a circle to represent the environment
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.screen_width / 2), int(self.screen_height / 2)),
                               int(self.screen_width / 2), 1)

            # Draw radiating lines from the center of the circle
            num_lines = 24  # Increase the number of lines
            line_length = int(self.screen_width / 2)  # Length of each line
            line_color = (192, 192, 192)  # Light grey color

            for angle in range(0, 360, 360 // num_lines):
                # Calculate the endpoint of each line based on the angle
                x_end = int(self.screen_width / 2 + line_length * np.cos(np.radians(angle)))
                y_end = int(self.screen_height / 2 + line_length * np.sin(np.radians(angle)))
                pygame.draw.line(self.screen, line_color, (int(self.screen_width / 2), int(self.screen_height / 2)),
                                 (x_end, y_end), 1)

            # Draw the blue and red dots inside the circle
            pygame.draw.circle(self.screen, (141, 144, 226), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_radius)
            pygame.draw.circle(self.screen, (158, 50, 90), (int(self.red_dot_pos[0]), int(self.red_dot_pos[1])),
                               self.red_dot_radius)

            # Draw the pink food
            pygame.draw.circle(self.screen, (255, 105, 180), (int(self.food_position[0]), int(self.food_position[1])),
                               self.food_radius)

            # Draw the blue dot search radius
            pygame.draw.circle(self.screen, (0, 0, 255), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_search_radius, 1)

            # Display the current blue dot's reward
            reward_text = f"Reward: {self.total_reward:.2f} Blue Health: {self.blue_dot_health}"
            text_surface = self.font.render(reward_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.screen_width - 200, 10)
            self.screen.blit(text_surface, text_rect)

            # Update the display
            pygame.display.update()

    # def close(self):
    #     # pygame.quit()
    #     pass


# Example usage of the gym environment
if __name__ == "__main__":
    env = DotEnv()
    done = False
    obs = env.reset()
    total_reward = 0
    steps = 0
    while not done:

        action_blue = env.action_space.sample()

        action = action_blue

        observation, reward, done, _, _ = env.step(action)
        total_reward += reward
        steps += 1
        env.render()

        # if env.blue_dot_health == 0:
        #     env.close()
    print(f'total reward: {total_reward}. total steps: {steps}')
    env.close()


