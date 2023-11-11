import math
import numpy as np
# import pygame
from Constants.constants import SCREEN_WIDTH, GREEN

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

#
# class CastRays:
#     def __init__(self, screen):
#         self.screen = screen
#         self.agent_center = None
#         self.num_rays = None
#         self.ray_angles = None
#         self.ray_lengths = None
#
#     def update_cast_rays(self, agent, walls):
#         # agent and walls here are objects not list or anything
#         start_angle = agent.angle - 65  # 65 degrees to the left
#         end_angle = agent.angle + 65  # 65 degrees to the right
#         # angle_step = 130 / (num_rays - 1) if num_rays > 1 else 0  # Adjust the angle step for the number of rays
#         angle_step = np.abs((start_angle - end_angle) / 13)
#
#         ray_angles = np.arange(start_angle, end_angle + angle_step, angle_step).tolist()  # Convert to a Python list
#         ray_angles = [ray % 360 for ray in ray_angles]
#         self.ray_angles = ray_angles
#         self.num_rays = len(ray_angles)
#
#         ray_lengths = []
#
#         for angle in ray_angles:
#
#             angle = math.radians(angle)
#             ray_direction = np.array([math.cos(angle), math.sin(angle)], dtype=np.float32)
#
#             ray_direction /= np.linalg.norm(ray_direction)  # Normalize the direction vector
#
#             length = float('inf')  # Initialize length to infinity
#
#             for wall in walls:
#                 x1, y1 = agent.current_position
#                 self.agent_center = (int(x1), int(y1))
#                 x2, y2 = agent.current_position + SCREEN_WIDTH * ray_direction  # Set an initial endpoint far away
#
#                 x3, y3, x4, y4 = wall['x'], wall['y'], wall['width'], wall['height']
#
#                 den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
#
#                 if den == 0:
#                     continue
#
#                 t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
#                 u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
#
#                 if 0 <= t <= 1 and 0 <= u <= 1:
#                     intersection_point = np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
#                     # print('inside intersect')
#                     wall_length = np.linalg.norm(intersection_point - agent.current_position)
#                     if wall_length < length:
#                         length = wall_length
#
#             if length == float('inf'):
#                 length = SCREEN_WIDTH
#
#             ray_lengths.append(length)
#             self.ray_lengths = ray_lengths
#
#
#
#         return ray_angles, ray_lengths
#
#     # def draw_rays(self):
#     #     # print(self.intersect_points)
#     #     for ray_length, ray_angle in zip(self.ray_lengths, self.ray_angles):
#     #
#     #         ray_angle = math.radians(ray_angle)
#     #         end_point = (int(math.cos(ray_angle) * ray_length), int(math.sin(ray_angle)) * ray_length)
#     #         ray_rect = pygame.draw.line(self.screen, GREEN, self.agent_center, end_point)
#





def update_cast_rays(agent, walls):
    start_angle = agent.angle - 65  # 65 degrees to the left
    end_angle = agent.angle + 65  # 65 degrees to the right
    # angle_step = 130 / (num_rays - 1) if num_rays > 1 else 0  # Adjust the angle step for the number of rays
    angle_step = np.abs((start_angle - end_angle) / 13)

    ray_angles = np.arange(start_angle, end_angle + angle_step, angle_step).tolist()  # Convert to a Python list
    # ray_angles = [ray % 360 for ray in ray_angles]
    ray_lengths = []

    for angle in ray_angles:

        angle = math.radians(angle)
        ray_direction = np.array([math.cos(angle), math.sin(angle)], dtype=np.float32)

        ray_direction /= np.linalg.norm(ray_direction)  # Normalize the direction vector

        length = float('inf')  # Initialize length to infinity

        for wall in walls:
            x1, y1 = agent.current_position
            x2, y2 = agent.current_position + SCREEN_WIDTH * ray_direction  # Set an initial endpoint far away

            x3, y3, x4, y4 = wall['x'], wall['y'], wall['x'] + wall['width'], wall['y'] + wall['height']

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if den == 0:
                continue

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if 0 <= t <= 1 and 0 <= u <= 1:
                intersection_point = np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
                # print('inside intersect')
                wall_length = np.linalg.norm(intersection_point - agent.current_position)
                if wall_length < length:
                    length = wall_length

        if length == float('inf'):
            length = SCREEN_WIDTH

        ray_lengths.append(length)

    return ray_angles, ray_lengths

