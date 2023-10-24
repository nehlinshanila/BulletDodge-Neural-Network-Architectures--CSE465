from gymnasium.spaces import Discrete, Box
from gymnasium import Env
import numpy as np
import pygame

from Agents.agent import Agent

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class GameEnv(Env):
    def __init__(self, screen_width=400, screen_height=400, render_mode='human'):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        # defining the observation and action spaces for all the agents
        self.action_space = Discrete(4)
        self.observation_space = Box(low=np.array([0, 0, 0, 0], dtype=np.float32),
                                     high=np.array(
                                         [self.screen_width, self.screen_height, self.screen_width, self.screen_height],
                                         dtype=np.float32),
                                     dtype=np.float32)

        # the pygame window should be initialized in the render function

        # setting the total number of agent

        self.number_of_prey = 1
        self.number_of_predator = 1
        self.prey_agents = []
        self.predator_agents = []
        self.number_of_agents = self.number_of_prey + self.number_of_prey

        # if self.number_of_prey > 0 and self.number_of_predator > 0:
        #     self.agent_init()
        # else:
        #     self.prey_agents.append(Agent('prey', 0))
        #     self.predator_agents.append(Agent('predator', 0))

        # setting the total number of obstacles
        self.total_obstacles = None

        # keeping a counter to save the total steps
        self.total_steps = 0

        # initializing the pygame
        pygame.init()

        # setting the screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Multi Agent Environment(simple)')

        # initializing the font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def agent_init(self):
        # initializing all the agents
        prey_agents = []
        predator_agents = []

        for i in range(0, self.number_of_prey):
            agent = Agent('prey', i)
            prey_agents.append(agent)

        for i in range(0, self.number_of_predator):
            agent = Agent('predator', i)
            predator_agents.append(agent)

        self.prey_agents = prey_agents
        self.predator_agents = predator_agents

    def set_agent_number(self, prey_number, predator_number):
        self.number_of_predator = predator_number
        self.number_of_prey = prey_number

    def reset(self, seed=0):
        self.total_steps = 0
        observation = []

        for prey in self.prey_agents:
            prey.agent_reset(width=self.screen_width, height=self.screen_height)
            observation.append([prey.index, prey.agent, prey.current_position])

        for predator in self.predator_agents:
            predator.agent_reset(width=self.screen_width, height=self.screen_height)
            observation.append([predator.index, predator.agent, predator.current_position])

        return observation, seed

    def step(self, action):
        observation = []

        prey_actions, predator_actions = action

        for prey, action in zip(self.prey_agents, prey_actions):
            print(f"prey_{prey.index} = action:{action} current_position: {prey.current_position}")
            prey.step_update(action=action, low=self.observation_space.low, high=self.observation_space.high)
            print(f'prey_{prey.index}: new_position: {prey.current_position}')

            observation.append([prey.index, prey.agent, prey.current_position])

        for predator, action in zip(self.predator_agents, predator_actions):
            print(f'predator_{predator.index} = action:{action} current_position: {predator.current_position}')
            predator.step_update(action=action, low=self.observation_space.low, high=self.observation_space.high)
            print(f'predator_{predator.index}: new_position: {predator.current_position}')

            observation.append([predator.index, predator.agent, predator.current_position])

        self.total_steps += 1

        done = False
        reward = 0.00
        truncated = False
        info = {}

        print(self.total_steps)

        return observation, reward, done, truncated, info

    def render(self):
        if self.render_mode == 'human':
            screen = self.screen

            # clear screen
            screen.fill((255, 255, 255))

            for prey in self.prey_agents:
                pos_x, pos_y = prey.current_position
                prey_radius = 10
                pygame.draw.circle(screen, (0, 0, 255), (int(pos_x), int(pos_y)), prey_radius)

            for predator in self.predator_agents:
                pos_x, pos_y = predator.current_position
                predator_radius = 10

                pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), predator_radius)

            pygame.display.update()

    def close(self):
        pygame.quit()
