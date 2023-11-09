import numpy as np
import math
import pygame as pg
from bullets import Bullet
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Constants.constants import GREEN
class Turret:
    def __init__(self, screen, width, height):
        self.pos_x = width / 2
        self.pos_y = height / 2
        self.position = np.array([self.pos_x, self.pos_y], dtype=np.float32)
        self.screen = screen
        self.angle = 0
        self.radius = 15

        self.shoot_interval = 2  # shooting interval of the turret
        self.center = (int(self.pos_x), int(self.pos_y))

        self.rect = pg.draw.circle(screen, GREEN, self.center, self.radius)

        self.bullet_pos = (self.center[0] + self.radius * math.cos(math.radians(self.angle)),
                           self.center[1] + self.radius * math.sin(math.radians(self.angle)))

        self.bullets = []

    def rotate_turret(self, end_point=None):
        """
        the end_point here gives a position coordinate (x, y)
        this needs to be used for the turret direction
        """

        magnitude = 30
        angle = math.radians(self.angle)
        # angle = self.angle
        dir_vec_x = magnitude * math.cos(angle)
        dir_vec_y = magnitude * math.sin(angle)

        direction_end = (self.center[0] + dir_vec_x, self.center[1] + dir_vec_y)

        self.bullet_pos = (
        self.center[0] + self.radius * math.cos(angle), self.center[1] + self.radius * math.sin(angle))
        # self.bullet_pos = direction_end / 2

        return direction_end

    def shoot(self):
        bullet = Bullet(*self.bullet_pos, self.angle, self.screen)
        self.bullets.append(bullet)
        # if shooting interval is 2 then shoot at the current angle

    def get_bullets(self):
        return self.bullets

    def destroy_bullet(self, bullet):
        self.bullets.remove(bullet)
