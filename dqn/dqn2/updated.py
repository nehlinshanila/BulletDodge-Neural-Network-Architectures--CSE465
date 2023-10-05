import gym
import numpy as np
from gym import spaces
import pygame
import random
import time

# only 1 food at a time.
# set a timelimit
# increase blue speed by a lot
# eats one food reward increases
# after eating every 5 food gets a huge bonus
# after not eating till time over, reward decreases rapidly
# will teach blue dot not to roam around too much and eat
# try setting the best snake hyperparameters on net

class DotEnv(gym.Env):
    def __init__(self, screen_width=700, screen_height=700, render_mode='human'):
        super(DotEnv, self).__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        self.direction_line_length = 20
        self.game_speed = 1
        self.test_health = 50

        self.blue_dot_radius = 30
        self.blue_dot_health = 50
        self.blue_dot_attack_dmg = 1
        self.blue_dot_search_radius = 100
        self.blue_dot_turn_rate = None
        self.blue_dot_stamina = 50
        self.blue_dot_stamina_recovery_rate = 15
        self.blue_dot_pos_prev = None

        self.food_radius = 20
        self.food_positions = []  # List to store food positions
        self.food_types = []  # List to store food types ('pink', 'green', 'yellow')
        self.food_effects = []  # List to store food effects (1: increase health, -1: decrease health, 2: speed boost)

        self.eaten_food = 0  # Variable to keep track of eaten food

        self.food_reward = 100  # Reward for collecting pink (edible) food
        self.green_food_penalty = -50  # Penalty for collecting green (inedible) food

        self.food_regeneration_interval = 10  # Regenerate food every 10 seconds
        self.last_food_regeneration_time = 0

        self.max_food_count = 10

        self.action_space = spaces.Discrete(4)

        self.observation_space = spaces.Box(low=np.array([0, 0], dtype=np.float32),
                                            high=np.array([self.screen_width / 2, self.screen_height],
                                                          dtype=np.float32),
                                            dtype=np.float32)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dots Moving Environment')

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.total_reward = 0
        self.speed_boost_timer = 0  # Initialize the speed boost timer

        for _ in range(self.max_food_count):
            self.spawn_food()

    def spawn_food(self):
        while True:
            food_position = np.array(
                [random.uniform(0, self.screen_width), random.uniform(0, self.screen_height)],
                dtype=np.float32)
            if np.linalg.norm(
                    food_position - np.array([self.screen_width / 2, self.screen_height / 2])) < int(
                self.screen_width / 2) - self.food_radius:
                food_type = random.choice(['pink', 'green', 'yellow'])
                self.food_positions.append(food_position)
                self.food_types.append(food_type)

                if food_type == 'pink':
                    food_effect = 1
                elif food_type == 'green':
                    food_effect = -1
                else:
                    food_effect = 2

                self.food_effects.append(food_effect)
                break

    def reset(self, seed=0):
        super().reset(seed=seed)

        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.blue_dot_health = 50

        self.food_positions = []
        self.food_types = []
        self.food_effects = []

        for _ in range(self.max_food_count):
            self.spawn_food()

        self.total_reward = 0
        self.speed_boost_timer = 0  # Reset the speed boost timer

        self.last_food_regeneration_time = time.time()  # Reset the food regeneration timer
        self.eaten_food = 0  # Reset eaten food count

        return np.copy(self.blue_dot_pos)

    def step(self, action):
        action_blue_dot = action

        move_speed = 0.9 * self.game_speed

        prev_blue_dot_pos = np.copy(self.blue_dot_pos)

        if action_blue_dot == 0:
            self.blue_dot_pos[0] -= move_speed
        elif action_blue_dot == 1:
            self.blue_dot_pos[0] += move_speed
        elif action_blue_dot == 2:
            self.blue_dot_pos[1] -= move_speed
        elif action_blue_dot == 3:
            self.blue_dot_pos[1] += move_speed

        distance_to_center = np.linalg.norm(
            self.blue_dot_pos - np.array([int(self.screen_width / 2), int(self.screen_height / 2)]))
        if distance_to_center > int(self.screen_width / 2):
            self.blue_dot_pos = self.blue_dot_pos - 2 * (
                    self.blue_dot_pos - np.array([int(self.screen_width / 2), int(self.screen_height / 2)]))

        food_rewards = []
        for i in range(len(self.food_positions)):
            food_position = self.food_positions[i]
            food_type = self.food_types[i]
            food_effect = self.food_effects[i]

            distance_to_food = np.linalg.norm(self.blue_dot_pos - food_position)

            # Check if the blue dot has collected the food
            if distance_to_food < self.blue_dot_radius + self.food_radius:
                if food_type == 'pink':
                    self.total_reward += 50
                    self.blue_dot_health = min(100, self.blue_dot_health + food_effect)
                elif food_type == 'green':
                    self.total_reward -= 50
                    self.blue_dot_health = max(0, self.blue_dot_health - food_effect)
                elif food_type == 'yellow':
                    self.total_reward += 10  # You can change this if yellow food has a different reward
                    self.speed_boost_timer = 10  # Set the speed boost timer to 10 seconds
                    move_speed += food_effect

                self.eaten_food += 1  # Increment eaten food count

                del self.food_positions[i]
                del self.food_types[i]
                del self.food_effects[i]

                break
            else:
                # Calculate reward based on proximity to the food
                reward = 0
                if distance_to_food < self.blue_dot_search_radius:
                    if food_type == 'pink':
                        reward += 0.5  # Increase reward for being close to pink food
                    elif food_type == 'green':
                        reward -= 0.5  # Decrease reward for being close to green food
                    elif food_type == 'yellow':
                        reward += 0.2  # Increase reward for being close to yellow food
                food_rewards.append(reward)

        # Decrement the speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                # Speed boost has expired, reset the speed back to normal
                move_speed = 0.9 * self.game_speed

        direction = self.blue_dot_pos - np.array([int(self.screen_width / 2), int(self.screen_height / 2)])
        direction /= np.linalg.norm(direction)

        # Check if it's time to regenerate food
        current_time = time.time()
        if current_time - self.last_food_regeneration_time >= self.food_regeneration_interval:
            # Regenerate food items
            self.spawn_food()
            self.last_food_regeneration_time = current_time  # Update the food regeneration timer

        self.blue_dot_pos[0] = np.clip(self.blue_dot_pos[0], 0, self.screen_width / 2)
        self.blue_dot_pos[1] = np.clip(self.blue_dot_pos[1], 0, self.screen_height)

        observation = np.copy(self.blue_dot_pos)

        done = self.blue_dot_health == 0

        return observation, self.total_reward, done, {}

    def display_total_reward(self):
        reward_text = f"Current Reward: {self.total_reward:.2f}"
        text_surface = self.font.render(reward_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.screen_width - 200, 10)
        self.screen.blit(text_surface, text_rect)

    def render(self):
        if self.render_mode == 'human':
            self.screen.fill((93, 97, 140))

            pygame.draw.circle(self.screen, (234, 222, 255), (int(self.screen_width / 2), int(self.screen_height / 2)),
                               int(self.screen_width / 2) - 1)

            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.screen_width / 2), int(self.screen_height / 2)),
                               int(self.screen_width / 2), 1)

            num_lines = 24
            line_length = int(self.screen_width / 2)
            line_color = (192, 192, 192)

            for angle in range(0, 360, 360 // num_lines):
                x_end = int(self.screen_width / 2 + line_length * np.cos(np.radians(angle)))
                y_end = int(self.screen_height / 2 + line_length * np.sin(np.radians(angle)))
                pygame.draw.line(self.screen, line_color, (int(self.screen_width / 2), int(self.screen_height / 2)),
                                 (x_end, y_end), 1)

            pygame.draw.circle(self.screen, (141, 144, 226), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_radius)

            for i in range(len(self.food_positions)):
                food_position = self.food_positions[i]
                food_type = self.food_types[i]
                if food_type == 'pink':
                    food_color = (255, 105, 180)
                elif food_type == 'green':
                    food_color = (0, 128, 0)
                elif food_type == 'yellow':
                    food_color = (255, 255, 0)
                pygame.draw.circle(self.screen, food_color, (int(food_position[0]), int(food_position[1])),
                                   self.food_radius)

            pygame.draw.circle(self.screen, (0, 0, 255), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_search_radius, 1)

            self.display_total_reward()

            pygame.display.update()

if __name__ == "__main__":
    env = DotEnv(screen_width=700, screen_height=700, render_mode='human')
    env.reset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        env.render()

        if done:
            env.reset()

    pygame.quit()
