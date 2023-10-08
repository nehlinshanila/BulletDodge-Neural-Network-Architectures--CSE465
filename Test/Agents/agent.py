import numpy as np


class Agent:
    def __init__(self, agent_name, agent_index):
        self.index = agent_index
        self.agent = agent_name
        self.health = None
        self.isHit = False
        self.move = True
        self.movement_speed = 1.00
        self.previous_position = np.array([0, 0], dtype=np.float32)
        self.current_position = None
        self.same_position = False
        self.current_step = 0
        self.action = None
        pass

    def agent_action(self, action):

        pass

    def agent_update(self, step, action, width, height):
        if step > 0:
            if (self.previous_position != self.current_position).all():
                self.previous_position = self.current_position
                self.same_position = False

                if action:
                    self.step_update(action)
                else:
                    pass
            else:
                self.same_position = True

    def agent_reset(self, width, height=0):
        padding = 30
        self.current_position = np.array(
            [np.random.uniform(30, width - padding), np.random.uniform(30, width - padding)], dtype=np.float32)

    def step_update(self, action, range_x, range_y):

        if action == 0:
            self.current_position[0] -= self.movement_speed
        elif action == 1:
            self.current_position[0] += self.movement_speed
        elif action == 2:
            self.current_position[1] -= self.movement_speed
        elif action == 3:
            self.current_position[1] += self.movement_speed

        self.current_position[0] = np.clip(self.current_position[0], 0, range_x)
        self.current_position[1] = np.clip(self.current_position[1], 0, range_y)


