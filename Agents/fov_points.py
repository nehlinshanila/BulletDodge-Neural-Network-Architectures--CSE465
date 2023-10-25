import numpy as np
import time
import math

from Constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS, PREDATOR_RADIUS


def get_fov_points(agent_position):
    fov_points = {}
    x, y = agent_position
    for angle in range(360):
        radians = math.radians(angle)
        for r in range(PREDATOR_RADIUS + 1, FOV_RADIUS + 1):
            x_coord = int(x + r * math.cos(radians))
            y_coord = int(y + r * math.sin(radians))
            if 0 <= x_coord < SCREEN_WIDTH and 0 <= y_coord < SCREEN_HEIGHT:
                fov_points[(x_coord, y_coord)] = 0  # Inside FOV
            else:
                fov_points[(x_coord, y_coord)] = 1  # Outside FOV (outside screen)
    return fov_points



# run time
if __name__ == '__main__':
    # agent_pos = [50, 300]
    # count = 0
    # fov = get_fov_points(agent_pos)
    # print(len(fov))
    # for key, value in fov.items():
    #     if key[0] < 0:
    #         print(key[0], key[1])
    # print(count)
    agent_position = (250, 20)
    start_time = time.time()
    result = get_fov_points(agent_position)
    print(len(result))
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")

# if __name__ == '__main__':
#     agent_location = [328.8917, 301.3598]
#     print(get_fov_points(agent_location))


