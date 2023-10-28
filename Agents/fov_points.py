import numpy as np
import time
import math

from Constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS, PREDATOR_RADIUS


def get_fov_points(agent_position):
    fov_points = {}
    x, y = agent_position
    for angle in range(360):
        # Convert angle to radians
        radians = np.deg2rad(angle)
        # Calculate new coordinates within FOV based on polar coordinates 
        x_coord = int(x + 15 + FOV_RADIUS * np.cos(radians))
        y_coord = int(y + 15 + FOV_RADIUS * np.sin(radians))
        # Check if the calculated x_coord and y_coord fall within the screen boundaries.
        if 0 < x_coord < SCREEN_WIDTH and 0 < y_coord < SCREEN_HEIGHT:
            # If yes, then add the coordinates to the fov_points list
            fov_points[(x_coord, y_coord)] = 0
            # fov_points.append((x_coord, y_coord))
        else:
            fov_points[(x_coord, y_coord)] = 1

    return fov_points


if __name__ == '__main__':
    agent_pos = [20, 550]
    count = 0

    fov = get_fov_points(agent_pos)
    print(fov)

    # for key, value in fov.items():
    #     if key[0] > 600 and key[1] > 600:
    #         print(key[0], key[1], value)
    #         count += 1
    # print(count)
