import math

import numpy as np


class Agent:
    def __init__(self, agent_name, agent_index):
        # identity
        self.index = agent_index
        self.agent = agent_name

        # additional attributes
        self.health = None
        self.isHit = False
        self.move = True
        self.movement_speed = 1.00

        # positional attributes
        self.previous_position = np.array([0, 0], dtype=np.float32)
        self.current_position = None
        self.same_position = False

        self.current_step = 0
        self.action = None

        # these are for the angular motion of the agent
        self.angle = 0
        self.center = 0
        self.direction = 0
        self.direction_end = 0
        self.radius = 15

        # this is custom only for the render function
        self.draw_direction_end = 0

    # for handling what the action does
    def agent_action(self, action):
        pass

    def _get_min_left(self, walls):
        min_x = 1000
        for wall in walls:
            if wall.left < min_x:
                min_x = wall.left
        return min_x

    # for handling all the initial states
    def agent_reset(self, width, height):
        padding = 30
        # updating the initial random position of the agent at 1st
        # self.current_position = np.array(
        #     [np.random.uniform(30, self._get_min_left(walls)), np.random.uniform(30, height - padding)],
        #     dtype=np.float32)

        # self.current_position = np.array([40, height/2], dtype=np.float32)

        self.current_position = np.array([75, height-75], dtype=np.float32)

        # updating the initial orientation to 0 degree at 1st
        theta = math.radians(self.angle)
        magnitude = padding
        # this is for the trigonometry function X and Y
        dir_vec_x = magnitude * math.cos(theta)
        dir_vec_y = magnitude * math.sin(theta)

        # adding the direction vector to the center and get an end point for direction
        self.direction_end = np.array([self.current_position[0] + dir_vec_x, self.current_position[1] + dir_vec_y],
                                      dtype=np.float32)

        # this part is only for the render function
        self.draw_direction_end = (self.current_position[0] + dir_vec_x, self.current_position[1] + dir_vec_y)
        self.center = (int(self.current_position[0]), int(self.current_position[1]))

    # updating the direction, line-end according to given angle when called
    def get_direction(self):
        # as render function demands an int value
        center = (int(self.current_position[0]), int(self.current_position[1]))
        self.center = center

        # the X, Y angular equation
        theta = math.radians(self.angle)
        magnitude = 30
        # here is the X=cos()
        directional_vector_x = magnitude * math.cos(theta)
        # here is the Y=sin()
        directional_vector_y = magnitude * math.sin(theta)

        directional_line_end = np.array([center[0] + directional_vector_x, center[1] + directional_vector_y],
                                        dtype=np.float32)
        self.direction_end = directional_line_end

        direction = directional_line_end - center
        direction /= np.linalg.norm(direction)
        self.direction = direction
        self.draw_direction_end = (center[0] + directional_vector_x, center[1] + directional_vector_y)

    # for updating the states of the agent when called
    def step_update(self, action, range_x, range_y):

        # ! if used directional rotational movement
        # rotate clockwise
        if action == 0:

            self.angle += 10
            self.angle = self.angle % 360
            # self.get_direction()

        # rotate anti-clockwise
        elif action == 1:
            self.angle -= 10
            self.angle = self.angle % 360
            # self.get_direction()

        # move front
        elif action == 2:
            self.current_position = self.current_position + self.direction * self.movement_speed
            # self.get_direction()

        # move back
        # elif action == 3:
        #     self.current_position = self.current_position - self.direction * self.movement_speed
            # self.get_direction()

        # do nothing / wait
        # elif action == 4:
        #     pass

        self.get_direction()

        self.current_position[0] = np.clip(self.current_position[0], 10, range_x-10)
        self.current_position[1] = np.clip(self.current_position[1], 10, range_y-10)

    # this function returns all the state needed for the observations
    # ! can be changed with need for the algorithm
    def get_agent_state(self):

        agent_state = {
            'agent_id': self.index,
            'agent_name': self.agent,
            'agent_move_speed': self.movement_speed,
            'agent_current_position': self.current_position,
            'agent_angle': self.angle
        }

        return agent_state
