import os
import sys
import time

import numpy as np
import pygame
from gymnasium import Env
from gymnasium.spaces import Discrete, Dict, Box

from Agents.agent import Agent
# from Agents.fov_points import get_fov_points
from Agents.overlap_detection import detect_overlapping_points
from Constants.constants import WHITE, RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, WALLS, FOV_RADIUS
from Walls.collision_detection import detect_collision
from Walls.wall_class import Walls

# env essentials import
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class GameEnv(Env):
    def __init__(self, render_mode='human'):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.render_mode = render_mode

        # defining the observation and action spaces for all the agents
        self.observation_space = Dict({
            'predator_position': Box(low=np.array([0, 0], dtype=np.float32),
                                     high=np.array([SCREEN_WIDTH, SCREEN_HEIGHT], dtype=np.float32),
                                     dtype=np.float32),
            'vision': Dict({
                'vision_points': Discrete(2)
            }),
        })

        # defining the action space based on total number of predator and prey
        # since we are training only one agent so, defining only the necessary number of actions
        self.action_space = Discrete(5)
        # 5 for rotate
        # clockwise, anti-clock
        # move front, move back and wait

        self.total_steps = 0

        self.number_of_predator = 1

        self.predator_agent = None

        self.predator_total_reward = 0

        self.obs = None

        # start the tick timer
        self.start_time = 0
        self.total_running_time = 10

        # the pygame window should be initialized in the render function
        # initializing the pygame
        pygame.init()

        # setting the screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Multi Agent Environment(simple)')

        # initializing the font
        pygame.font.init()
        self.font = pygame.font.Font(None, 18)

        # for the wall initializations
        self.wall = Walls(pygame)
        self.walls = None

    def agent_init(self):
        predator_agents = Agent('predator', 0)

        self.predator_agent = predator_agents

    def _get_obs(self):
        observation = {
            'predator_position': self.predator_agent.current_position,
            'predator_angle': self.predator_agent.angle,
            'vision': detect_overlapping_points(self.predator_agent.current_position, WALLS),
        }

        return observation

    def _max_right(self):
        max_right = 0

        for wall in self.walls:
            if wall.right > max_right:
                max_right = wall.right
        return max_right

    # the usual reset function
    def reset(self, seed=0):
        self.start_time = time.time()

        self.agent_init()
        self.wall.clear_walls()
        self.walls = self.wall.make_wall(WALLS)

        self.total_steps = 0
        self.predator_total_reward = 0

        predator = self.predator_agent

        # for predator in self.predator_agents:
        predator.agent_reset(width=self.screen_width, height=self.screen_height, walls=self.walls)
        # observation.append([predator.index, predator.agent, predator.current_position])

        # setting the predator and prey to their initial position

        self.predator_agent = predator


        # all the variable values inside the observation space needs to be sent inside the observation variable
        # for this level purpose we decided to add the dictionary observation
        # set the observation to a dictionary
        observation = self._get_obs()
        self.obs = observation

        return observation, seed

    def step(self, action):
        # initializing the return variables
        done = False
        reward = 0
        truncated = False
        info = {}
        current_time = time.time()

        elapsed_time = current_time - self.start_time
        # handles the pygame window event when closing
        # !if the window still crashes pygame.event needs to be managed properly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
        self.predator_agent.step_update(action, range_x=self.screen_width, range_y=self.screen_height)
        self.predator_agent = detect_collision(self.predator_agent, self.walls)

        # observation needs to be set a dictionary

        self.total_steps += 1
        print(self._max_right())
        # for wall in self.walls:
        if self.predator_agent.current_position[0] > self._max_right():
            reward += 100
            done = True

        if elapsed_time >= self.total_running_time:
            done = True
        """
        here lies the most important task
        handling the rewards
        """
        reward += 0.01
        self.render()

        # it will update the total reward every step
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

            for key, wall in WALLS.items():
                pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))

            pygame.display.update()

    def close(self):
        pygame.quit()
