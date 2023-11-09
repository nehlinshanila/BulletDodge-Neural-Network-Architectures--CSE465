import math
import numpy as np
import sys
import pygame
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Walls.wall_class import Walls
from Constants.constants import LEVEL_4_WALLS, SCREEN_WIDTH, SCREEN_HEIGHT
from Agents.agent import Agent
# Create walls
wall = Walls(pygame)
walls = wall.make_wall(LEVEL_4_WALLS)

# Create the agent
agent = Agent("shanila", 15)
agent.agent_reset(SCREEN_WIDTH, SCREEN_HEIGHT, walls)


def cast_and_update_rays(agent, num_rays, walls):
    start_angle = agent.angle - 65  # 65 degrees to the left
    end_angle = agent.angle + 65  # 65 degrees to the right
    angle_step = 130 / (num_rays - 1) if num_rays > 1 else 0  # Adjust the angle step for the number of rays

    ray_angles = np.arange(start_angle, end_angle + angle_step, angle_step).tolist()  # Convert to a Python list
    ray_lengths = []

    for angle in ray_angles:
        ray_direction = np.array([math.cos(math.radians(angle)), math.sin(math.radians(angle))])
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
                wall_length = np.linalg.norm(intersection_point - agent.current_position)
                if wall_length < length:
                    length = wall_length  

        if length == float('inf'):
            length = SCREEN_WIDTH  
        ray_lengths.append(length)

    return ray_angles, ray_lengths

