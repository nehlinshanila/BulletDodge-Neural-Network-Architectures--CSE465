import gym
import numpy as np
import pygame
import random
import time


class DotEnv(gym.Env):
    def __init__(self, screen_width=700, screen_height=700, render_mode='human'):
        super(DotEnv, self).__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        self.blue_dot_radius = 30
        self.blue_dot_health = 50
        self.blue_dot_speed = 2.0  # Increased speed
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        self.food_radius = 20
        self.food_positions = []  # List to store food positions
        self.food_types = []  # List to store food types ('pink', 'green')

        self.eaten_pink_food = 0
        self.reward_bonus_interval = 5  # Bonus reward every 5 pink foods

        self.time_limit = 10  # Episode time limit in seconds
        self.episode_start_time = 0

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0], dtype=np.float32),
            high=np.array([self.screen_width / 2, self.screen_height], dtype=np.float32),
            dtype=np.float32
        )

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dots Moving Environment')

        self.font = pygame.font.Font(None, 36)
        self.total_reward = 0

        self.max_food_count = 2  # Maximum of 2 food items (1 pink, 1 green)

        self.reset()

    def spawn_food(self):
        while True:
            food_position = np.array(
                [random.uniform(self.screen_width / 4, self.screen_width / 2), random.uniform(0, self.screen_height)],
                dtype=np.float32)
            if np.linalg.norm(food_position - self.blue_dot_pos) < int(self.screen_width / 4) - self.food_radius:
                food_type = 'pink' if len(self.food_positions) % 2 == 0 else 'green'
                self.food_positions.append(food_position)
                self.food_types.append(food_type)
                break

    def reset(self, seed=None):
        self.episode_start_time = time.time()
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.food_positions = []
        self.food_types = []
        self.total_reward = 0
        self.eaten_pink_food = 0
        for _ in range(self.max_food_count):
            self.spawn_food()
        return np.copy(self.blue_dot_pos)

    def step(self, action):
        elapsed_time = time.time() - self.episode_start_time

        move_speed = self.blue_dot_speed

        if action == 0:
            self.blue_dot_pos[0] -= move_speed
        elif action == 1:
            self.blue_dot_pos[0] += move_speed
        elif action == 2:
            self.blue_dot_pos[1] -= move_speed
        elif action == 3:
            self.blue_dot_pos[1] += move_speed

        distance_to_center = np.linalg.norm(
            self.blue_dot_pos - np.array([int(self.screen_width / 4), int(self.screen_height / 2)]))
        if distance_to_center > int(self.screen_width / 4):
            self.blue_dot_pos = self.blue_dot_pos - 2 * (
                        self.blue_dot_pos - np.array([int(self.screen_width / 4), int(self.screen_height / 2)]))

        reward = 0
        for i in range(len(self.food_positions)):
            food_position = self.food_positions[i]
            food_type = self.food_types[i]
            distance_to_food = np.linalg.norm(self.blue_dot_pos - food_position)

            if distance_to_food < self.blue_dot_radius + self.food_radius:
                if food_type == 'pink':
                    reward += 10  # Increased reward for eating pink
                    self.eaten_pink_food += 1
                    self.total_reward += reward
                    self.food_positions.pop(i)
                    self.food_types.pop(i)
                elif food_type == 'green':
                    reward -= 10  # Penalty for eating green
                    self.total_reward += reward
                    self.food_positions.pop(i)
                    self.food_types.pop(i)
                break
            else:
                if distance_to_food < self.blue_dot_radius + self.food_radius * 2:
                    reward += 1  # Proximity reward

        if elapsed_time >= self.time_limit:
            reward -= 100  # Time's up penalty
            done = True
        else:
            done = False

        if self.eaten_pink_food % self.reward_bonus_interval == 0:
            reward += 50  # Bonus reward for every 5 pink foods

        observation = np.copy(self.blue_dot_pos)

        return observation, reward, done, {}

    def render(self):
        if self.render_mode == 'human':
            self.screen.fill((93, 97, 140))

            pygame.draw.circle(self.screen, (234, 222, 255), (int(self.screen_width / 4), int(self.screen_height / 2)),
                               int(self.screen_width / 4) - 1)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.screen_width / 4), int(self.screen_height / 2)),
                               int(self.screen_width / 4), 1)

            for i in range(len(self.food_positions)):
                food_position = self.food_positions[i]
                food_type = self.food_types[i]
                food_color = (255, 105, 180) if food_type == 'pink' else (0, 128, 0)
                pygame.draw.circle(self.screen, food_color, (int(food_position[0]), int(food_position[1])),
                                   self.food_radius)

            pygame.draw.circle(self.screen, (141, 144, 226), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_radius)

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
