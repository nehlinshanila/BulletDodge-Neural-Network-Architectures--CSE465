import numpy as np
import math

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class Bullet:
    def __init__(self, x, y, angle):
        self.width = 2
        self.height = 5
        self.angle = angle
        self.speed = 5
        # self.screen = screen
        self.pos_x = x
        self.pos_y = y
        self.pos = np.array([self.pos_x, self.pos_y], dtype=np.float32)
        self.center = (int(self.pos_x), int(self.pos_y))
        self.radius = 10

        # this rect object is for drawing
        # self.rect = pg.draw.circle(self.screen, RED, self.center, self.radius)

    def move(self):
        angle = math.radians(self.angle)
        # self.pos_x += self.speed * math.cos(angle)
        # self.pos_y += self.speed * math.sin(angle)
        # angle = self.angle
        dir_end_x = self.pos[0] + self.speed * math.cos(angle)
        dir_end_y = self.pos[1] + self.speed * math.sin(angle)

        dir_end = np.array([dir_end_x, dir_end_y], dtype=np.float32)
        direction = dir_end - self.pos
        direction /= np.linalg.norm(direction)

        # draw_dir_end = (int(dir_end_x), int(dir_end_y))

        # self.angle = self.angle % 360

        self.pos = self.pos + direction * self.speed
        # pos = (self.pos[0], self.pos[1])
        self.center = (int(self.pos[0]), int(self.pos[1]))

        # self.rect = pg.draw.circle(self.screen, RED, self.center, self.radius)
