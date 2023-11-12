import numpy as np
import math


class Bullet:
    def __init__(self, x, y, angle):
        self.width = 2
        self.height = 5
        self.angle = angle
        self.speed = 500
        # self.screen = screen
        self.pos_x = x
        self.pos_y = y
        self.pos = np.array([self.pos_x, self.pos_y], dtype=np.float32)
        self.center = (int(self.pos_x), int(self.pos_y))
        self.radius = 10

        # this rect object is for drawing
        # self.rect = pg.draw.circle(self.screen, RED, self.center, self.radius)

    def move(self, speed_factor):
        angle = math.radians(self.angle)
        # if speed_factor != 0.0000:
        #     self.speed = self.speed * speed_factor
        # dir_end_x = self.pos[0] + self.speed * math.cos(angle)
        # dir_end_y = self.pos[1] + self.speed * math.sin(angle)
        displacement = np.array([
            self.speed * speed_factor * math.cos(angle),
            self.speed * speed_factor * math.sin(angle)
        ], dtype=np.float32)

        # dir_end = np.array([dir_end_x, dir_end_y], dtype=np.float32)
        # direction = dir_end - self.pos
        # direction /= np.linalg.norm(direction)

        self.pos = self.pos + displacement

        self.center = (int(self.pos[0]), int(self.pos[1]))
