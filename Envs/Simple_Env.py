from gymnasium.spaces import Discrete, Box
from gymnasium import Env
import numpy as np
import pygame

from Agents.agent import Agent

import os
import sys
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class GameEnv(Env):
    def __init__(self, screen_width=400, screen_height=400, render_mode='human'):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        # defining the observation and action spaces for all the agents

        self.observation_space = Box(low=np.array([0, 0, 0, 0], dtype=np.float32),
                                     high=np.array(
                                         [self.screen_width, self.screen_height, self.screen_width, self.screen_height],
                                         dtype=np.float32),
                                     dtype=np.float32)

        # setting the total number of agent

        self.number_of_prey = 1
        self.number_of_predator = 1
        self.prey_agent = None
        self.predator_agent = None
        self.predator_i_position = None
        self.initial_distance = None
        self.current_distance = None
        self.previous_distance = None
        self.predator_total_reward = 0
        self.number_of_agents = self.number_of_prey + self.number_of_prey

        self.obs = None

        # defining the action space based on total number of predator and prey
        self.action_space = Discrete(4)

        # setting the total number of obstacles
        self.total_obstacles = None

        # keeping a counter to save the total steps
        self.total_steps = 0

        # the pygame window should be initialized in the render function
        # initializing the pygame
        pygame.init()

        # setting the screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Multi Agent Environment(simple)')

        # keep the track of time of the rendering
        self.clock = pygame.time.Clock()

        # *it is set in mily second format (time is sec is time/1000)
        self.total_running_time = 10

        # start the tick timer
        self.start_time = 0
        # print(f 'start time: {self.start_time}')

        # initializing the font
        pygame.font.init()
        self.font = pygame.font.Font(None, 18)

    # this function returns the value of the action into 2 digits
    # if the action_space.sample() gives 1 digit number
    # * if  the number is 3 it will return 03
    # * if  the number is 14 then it will return 14
    @staticmethod
    def expand_action_digit(action):

        # this basically checks the number if it has 1 then fills the rest with 0
        # if the number is 2 digits then it stays the same
        action = str(action).zfill(2)
        prey_action = int(action[0]) % 4
        predator_action = int(action[1]) % 4
        return prey_action, predator_action

    # this method will initialize the number of agents
    # ! this must be called from outside
    def agent_init(self):

        prey_agents = Agent('prey', 0)

        predator_agents = Agent('predator', 0)

        self.prey_agent = prey_agents
        self.predator_agent = predator_agents

    # this function is used to explicitly set the number of agents
    # ! this needs to be called from outside
    def set_agent_number(self, prey_number, predator_number):
        self.number_of_predator = predator_number
        self.number_of_prey = prey_number

    # the usual reset function
    def reset(self, seed=0):
        self.start_time = time.time()

        self.agent_init()

        self.total_steps = 0
        self.predator_total_reward = 0

        prey = self.prey_agent
        predator = self.predator_agent

        # for prey in self.prey_agents:
        prey.agent_reset(width=self.screen_width, height=self.screen_height)
        # observation.append([prey.index, prey.agent, prey.current_position])

        # for predator in self.predator_agents:
        predator.agent_reset(width=self.screen_width, height=self.screen_height)
        # observation.append([predator.index, predator.agent, predator.current_position])

        # setting the predator and prey to their initial position
        self.prey_agent = prey
        self.predator_agent = predator

        # setting the initial position of predator for reward
        self.predator_i_position = self.predator_agent.current_position

        # calculating the initial distance of 2 agents
        direction = self.predator_agent.current_position - self.prey_agent.current_position
        self.initial_distance = np.linalg.norm(direction)

        # all the variable values inside the observation space needs to be sent inside the observation variable
        observation = np.concatenate([self.prey_agent.current_position, self.predator_agent.current_position])
        self.obs = observation

        return observation, seed

    # the step function
    # this function is called for every time steps
    # this function updates the actions or states of agents in the env
    # this function is called default by the algorithms of all sorts
    # * it returns observation, reward, done, truncated, info
    # * any game policy change can be done here
    # * reward must be set here
    def step(self, action):

        # initializing the return variables
        done = False
        reward = 0
        truncated = False
        info = {}
        current_time = time.time()
        # print(f'current time: {current_time}')
        # when ever the step is starting set the start time
        # if self.total_steps == 0:
        #     self.start_time = pygame.time.get_ticks()
        # else:
        #     current_time = pygame.time.get_ticks()

        elapsed_time = current_time - self.start_time
        # print(f'elapsed time: {elapsed_time}')
        # handles the pygame window event when closing
        # !if the window still crashes pygame.event needs to be managed properly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

        # print(f'action: {action}')
        # *the actions are split as required
        # prey_action, predator_action = self.expand_action_digit(action)
        prey_action = action
        prey = self.prey_agent
        prey.step_update(action=prey_action, range_x=self.screen_width - 10, range_y=self.screen_height - 10)
        # print(f'prey: {prey_action}, predator: {predator_action}')


        predator = self.predator_agent
        # this is only when using another model's prediction
        # predator_action = model.predict(self.obs)
        # print(f'predator_{predator.index} = action:{action} current_position: {predator.current_position}')
        # predator.step_update(action=predator_action[0], range_x=self.screen_width - 10,
        # range_y=self.screen_height - 10)
        # print(f'predator_{predator.index}: new_position: {predator.current_position}')

        # !observation.append({'index': predator.index, 'name': predator.agent, 'position': predator.current_position})
        # observation = self.predator_agent.current_position
        observation = np.concatenate([self.prey_agent.current_position, self.predator_agent.current_position])

        # print(f'observation: {self.predator_agent.current_position}')
        self.total_steps += 1

        direction = self.predator_agent.current_position - self.prey_agent.current_position

        # Calculate the distance between the centers of the two dots
        distance_between_centers = np.linalg.norm(direction)
        # observation =  distance_between_centers

        self.current_distance = distance_between_centers

        if self.current_distance > self.initial_distance:
            self.initial_distance = self.current_distance
            reward += 0.01
        else:
            reward -= 0.01

        # check everystep if the distance of two agents are:
        # greater than  initial distance?
        # yes: -reward
        # no: +reward

        # if distance_between_centers > self.initial_distance:
        #     reward -= 0.06
        # else:
        #     reward += 0.01

        # Check if there is a collision (distance <= sum of radii)
        if elapsed_time <= self.total_running_time:
            if distance_between_centers <= 20:
                reward -= 50
                done = True
                # pygame.quit()
                # self.close()
            # if self.total_steps == 30000:
            #     done = True
        else:
            done = True
            reward += 100
            # pygame.quit()
            # self.close()

        # print(self.total_steps)
        self.render()
        # it will update the total reward every step
        self.predator_total_reward = reward
        self.obs = observation

        return observation, reward, done, truncated, info

    def render(self):
        if self.render_mode == 'human':
            screen = self.screen

            # clear screen
            screen.fill((255, 255, 255))
            prey = self.prey_agent
            pos_x, pos_y = prey.current_position
            prey_radius = 10
            pygame.draw.circle(screen, (0, 0, 255), (int(pos_x), int(pos_y)), prey_radius)

            predator = self.predator_agent
            pos_x, pos_y = predator.current_position
            predator_radius = 10

            pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), predator_radius)

            text_surface = self.font.render(
                f"Reward: {self.predator_total_reward: .5f} initial distance: {self.initial_distance: .2f} current_distance:{self.current_distance: .2f}",
                True, (0, 0, 0))

            text_rect = text_surface.get_rect()

            text_rect.center = (self.screen_width - 200, 10)

            self.screen.blit(text_surface, text_rect)

            pygame.display.update()

    def close(self):
        pygame.quit()
