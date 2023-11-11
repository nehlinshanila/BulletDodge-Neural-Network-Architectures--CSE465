import os
import sys
import time

import numpy as np
import pygame
# import gymnasium as gym
from gymnasium import Env
from gymnasium.spaces import Discrete, Dict, Box

from Agents.agent import Agent
from Constants.constants import WHITE, RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from Walls.collision_detection import detect_collision
from Walls.wall_class import Walls
from Entities.turret import Turret

sys.path.insert(1, os.path.join(sys.path[0], '..'))


class GameEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.observation_space = Dict({
            "predator_position": Box(low=np.array([0, 0], dtype=np.float32),
                                     high=np.array([self.screen_width, self.screen_height], dtype=np.float32),
                                     dtype=np.float32),

            "predator_angle": Discrete(360),

            "bullet_position": Box(low=np.array([0, 0], dtype=np.float32),
                                   high=np.array([self.screen_width, self.screen_height], dtype=np.float32),
                                   dtype=np.float32),

            "target_position": Box(low=np.array([0, 0], dtype=np.float32),
                                   high=np.array([self.screen_width, self.screen_height], dtype=np.float32),
                                   dtype=np.float32),
        })

        self.action_space = Discrete(3)

        self.total_steps = 0
        self.predator_agent = Agent('predator', 0)
        self.predator_total_reward = 0

        self.obs = None

        self.start_time = 0
        self.total_running_time = 10

        self.window = None
        self.clock = None

        # for the wall initializations
        self.wall = Walls(pygame)
        self.walls = None

        self.turret = Turret(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bullet = self.turret.get_bullets()

    def _get_obs(self):

        if len(self.bullet) == 1:
            bullet_pos = self.bullet[0].center
        else:
            bullet_pos = self.turret.center

        observation = {
            "predator_position": self.predator_agent.current_position,
            "predator_angle": self.predator_agent.angle,
            "bullet_position": bullet_pos,  # get bullet position
            "target_position": self.turret.center,  # get the main target position
        }
        print(f'observation:{observation}')
        return observation

    # def _get_info(self):
    #     distance = 10000
    #     self.goal_seen = is_ray_blocked(self.predator_agent.current_position, self.goal_coordinate, self.walls)
    #     if self.goal_seen:
    #         direction = self.goal_coordinate - self.predator_agent.current_position
    #         distance = np.linalg.norm(direction)
    #
    #     info = {
    #         "goal_seen": self.goal_seen,
    #         "distance": distance,
    #         "vision_blocked": not self.goal_seen,
    #     }
    #     # print(f'info: {info}')
    #     return info

    def get_reward(self, reward, done):
        bullet_pos = 0
        if len(self.bullet) == 1:
            bullet_pos = self.bullet[0].center
        else:
            bullet_pos = self.turret.center

        if np.linalg.norm(np.abs(self.predator_agent.center - bullet_pos)) < self.predator_agent.radius + self.bullet[0].radius:
            self.turret.destroy_bullet(self.bullet[0])
            reward -= 50
            done = True

        if np.linalg.norm(np.abs(self.predator_agent.center - self.turret.center)) < self.predator_agent.radius + self.turret.radius:
            reward += 100
            done = True

        return reward, done

    def reset(self, seed=None, option=None):
        super().reset(seed=seed)
        self.start_time = time.time()

        self.wall.clear_walls()
        self.walls = self.wall.make_wall(LEVEL_4_WALLS)

        self.total_steps = 0
        self.predator_total_reward = 0
        # self.total_seen = 0

        # for predator in self.predator_agents:
        self.predator_agent.agent_reset(width=self.screen_width, height=self.screen_height)
        self.turret.rotate_turret(self.predator_agent.center)

        # all the variable values inside the observation space needs to be sent inside the observation variable
        # for this level purpose we decided to add the dictionary observation
        # set the observation to a dictionary
        observation = self._get_obs()
        # info = self._get_info()

        return observation, {}

    def step(self, action):
        # initializing the return variables
        done = False
        reward = 0
        truncated = False
        info = {}
        current_time = time.time()

        elapsed_time = current_time - self.start_time

        self.predator_agent.step_update(action, range_x=self.screen_width, range_y=self.screen_height)
        self.predator_agent = detect_collision(self.predator_agent, self.walls)

        if len(self.turret.get_bullets()) == 0:
            self.turret.shoot()

        self.bullet[0].move()
        # if np.linalg.norm(np.abs(self.predator_agent.center - self.bullet[0].center)) < self.predator_agent.radius + self.bullet[0].radius:

        # observation needs to be set a dictionary

        self.total_steps += 1
        reward, done = self.get_reward(reward, done)

        if elapsed_time >= self.total_running_time:
            reward -= 100
            done = True

        # getting observation and info
        observation = self._get_obs()
        # info = self._get_info()

        self.predator_total_reward = reward
        self.obs = observation

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, done, truncated, info

    def render(self):
        if self.render_mode == 'rgb_array':
            self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.font.init()

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        screen = pygame.Surface((self.screen_width, self.screen_height))
        screen.fill(WHITE)

        # for the predator
        predator = self.predator_agent
        pygame.draw.circle(screen, RED, predator.center, predator.radius)
        pygame.draw.line(screen, RED, predator.center, predator.draw_direction_end, 5)

        # for turret
        pygame.draw.circle(screen, (0, 255, 0), self.turret.center, self.turret.radius)
        pygame.draw.line(screen, (0, 255, 0), self.turret.center, self.turret.rotate_turret(predator.center), 4)

        if len(self.bullet) != 0:
            pygame.draw.circle(screen, (255, 255, 0), self.bullet[0].center, self.bullet.radius)

        for key, wall in LEVEL_4_WALLS.items():
            pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))

        if self.render_mode == "human":

            font = pygame.font.Font(None, 18)

            text_surface = font.render(f"Reward: {self.predator_total_reward: .5f} ", True, (0, 0, 0))

            text_rect = text_surface.get_rect()

            text_rect.center = (self.screen_width - 200, 10)

            screen.blit(text_surface, text_rect)
            self.window.blit(screen, screen.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # this part is to fix the fps of rendering
            # self.clock.tick(self.metadata["render_fps"])

        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(screen)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.font.quit()
            pygame.quit()
