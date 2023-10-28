import os
import sys
import time

import numpy as np
import pygame
import gymnasium as gym
from gymnasium import Env
from gymnasium.spaces import Discrete, Dict, Box

from Agents.agent import Agent
# from Agents.overlap_detection import detect_overlapping_points
from Agents.RayCast import get_fov_rays
from Constants.constants import WHITE, RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_2_WALLS
from Walls.collision_detection import detect_collision
from Walls.wall_class import Walls

# env essentials import
sys.path.insert(1, os.path.join(sys.path[0], '..'))

WALLS2 = LEVEL_2_WALLS

WALLS2 = LEVEL_2_WALLS


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
            # to send only the points for which he has to cross
            "destination_coordinates": Box(low=np.array([0, 0], dtype=np.float32),
                                           high=np.array([self.screen_width, self.screen_height], dtype=np.float32),
                                           dtype=np.float32),

        })

        self.action_space = Discrete(3)
        # 3 for
        # rotate clockwise, anti-clock
        # move front

        self.total_steps = 0
        self.predator_agent = Agent('predator', 0)
        self.predator_total_reward = 0

        self.obs = None

        # start the tick timer
        self.start_time = 0
        self.total_running_time = 10

        self.window = None
        self.clock = None

        # for the wall initializations
        self.wall = Walls(pygame)
        self.walls = None

        self.goal_seen = False

    def _flatten_list(self, nested_list):
        flattened_list = []
        for item in nested_list:
            if isinstance(item, list):
                flattened_list.extend(self._flatten_list(item))
            else:
                flattened_list.append(item)
        return flattened_list

    def _get_obs(self):
        observation = {
            "predator_position": self.predator_agent.current_position,
            "predator_angle": self.predator_agent.angle,
            "destination_coordinates": None,  # need to send a np.array for the goal to reach,
        }
        # print(observation)
        return observation

    # to capture all the info
    def _get_info(self):
        """
            need to add some code to calculate the distance from agent center to goal (x,y)
        """

        info = {
            "goal_seen": self.goal_seen,
            "distance": 450,
            "vision_blocked": not self.goal_seen,
        }

        return info

    def get_reward(self, reward):
        curve = -0.03
        ascend = 0.02
        clamp = 10

        reward = reward
        goal_coordinate = 0
        agent_pos = self.predator_agent.current_position
        
        if seen:
            direction = goal_coordinate -
            distance = np.linalg.norm(direction)
            reward += ascend * np.exp(curve * distance) - clamp

        if agent_pos[0] > goal_coordinate[0] and agent_pos[1] < goal_coordinate[1]:
            done = True
            reward = 200

        reward += 0.001

        print(f'direction: {direction}, distance:{distance}, reward: {reward}')
        return reward

    # the usual reset function
    def reset(self, seed=None, option=None):
        super().reset(seed=seed)
        self.start_time = time.time()

        self.wall.clear_walls()
        self.walls = self.wall.make_wall(WALLS2)

        self.total_steps = 0
        self.predator_total_reward = 0

        # for predator in self.predator_agents:
        self.predator_agent.agent_reset(width=self.screen_width, height=self.screen_height, walls=self.walls)

        # all the variable values inside the observation space needs to be sent inside the observation variable
        # for this level purpose we decided to add the dictionary observation
        # set the observation to a dictionary
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

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

        # observation needs to be set a dictionary

        self.total_steps += 1
        reward = self.get_reward(reward)

        if self.predator_agent.current_position[0] > self.walls[1].right:
            reward += 100
        # for wall in self.walls:
        if self.predator_agent.current_position[0] > self._max_right():
            reward += 200
            done = True

        if elapsed_time >= self.total_running_time + 10:
            reward -= 100
            done = True
        """
        here lies the most important task
        handling the rewards
        """

        # getting observation and info
        observation = self._get_obs()
        info = self._get_info()

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

        predator = self.predator_agent
        pygame.draw.circle(screen, RED, predator.center, predator.radius)
        pygame.draw.line(screen, RED, predator.center, predator.draw_direction_end, 5)

        mid_point = 0

        if self.predator_agent.current_position[0] < self.walls[0].midbottom[0]:
            mid_point = (np.array(self.walls[0].midbottom, dtype=np.float32) + np.array(self.walls[1].midtop,
                                                                                        dtype=np.float32)) / 2
            # print(f'mid point: {mid_point}')
            direction = mid_point - self.predator_agent.current_position

        if self.walls[0].right < self.predator_agent.current_position[0] < self.walls[2].midbottom[0]:
            mid_point = (np.array(self.walls[2].midbottom, dtype=np.float32) + np.array(self.walls[3].midtop,
                                                                                        dtype=np.float32)) / 2
            direction = mid_point - self.predator_agent.current_position
        mid_point = (int(mid_point[0]), int(mid_point[1]))
        pygame.draw.line(screen, RED, predator.center, mid_point, 2)

        for key, wall in WALLS2.items():
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