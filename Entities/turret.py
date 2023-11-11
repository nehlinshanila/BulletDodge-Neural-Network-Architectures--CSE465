import numpy as np
import math
from Entities.bullets import Bullet

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))


class Turret:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos_x = width / 2
        self.pos_y = height / 2
        self.position = np.array([self.pos_x, self.pos_y], dtype=np.float32)
        # self.screen = screen
        self.angle = 0
        self.radius = 15

        self.shoot_interval = 2  # shooting interval of the turret
        self.center = (int(self.pos_x), int(self.pos_y))

        # self.rect = pg.draw.circle(screen, GREEN, self.center, self.radius)

        self.bullet_pos = (self.center[0] + self.radius * math.cos(math.radians(self.angle)),
                           self.center[1] + self.radius * math.sin(math.radians(self.angle)))

        self.bullets = []

    def rotate_turret(self, end_point):
        """
        the end_point here gives a position coordinate (x, y)
        this needs to be used for the turret direction
        """

        magnitude = 30

        direction = end_point - self.position
        angle = math.atan2(direction[1], direction[0])
        angle = math.degrees(angle)
        angle = (angle + 360) % 360
        self.angle = angle
        angle = math.radians(angle)

        dir_vec_x = magnitude * math.cos(angle)
        dir_vec_y = magnitude * math.sin(angle)

        direction_end = (self.center[0] + dir_vec_x, self.center[1] + dir_vec_y)

        self.bullet_pos = (
            self.center[0] + self.radius * math.cos(angle), self.center[1] + self.radius * math.sin(angle))
        # self.bullet_pos = direction_end / 2

        return direction_end

    def shoot(self):
        bullet = Bullet(self.bullet_pos[0], self.bullet_pos[1], self.angle)
        self.bullets.append(bullet)

    def get_bullets(self):
        return self.bullets

    def auto_destroy(self):
        if self.bullets[0].pos[0] + self.bullets[0].radius > self.width or \
                self.bullets[0].pos[1] + self.bullets[0].radius > self.height or \
                self.bullets[0].pos[0] - self.bullets[0].radius < 0 or \
                self.bullets[0].pos[1] - self.bullets[0].radius < 0:
            self.destroy_bullet(self.bullets[0])

    def destroy_bullet(self, bullet):
        self.bullets.remove(bullet)
