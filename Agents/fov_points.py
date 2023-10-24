import numpy as np

from Constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS


# ! time complexity of O(n)
def get_fov_points(agent_position):
    fov_points = {}
    x, y = agent_position
    # Loop that iterates from 0 to 359, representing all possible angles in degrees.
    for angle in range(360):
        # Convert angle to radians
        radians = np.deg2rad(angle)
        # Calculate new coordinates within FOV based on polar coordinates 
        x_coord = int(x + FOV_RADIUS * np.cos(radians))
        y_coord = int(y + FOV_RADIUS * np.sin(radians))
        # Check if the calculated x_coord and y_coord fall within the screen boundaries.
        if 0 <= x_coord < SCREEN_WIDTH and 0 <= y_coord < SCREEN_HEIGHT:
            # If yes, then add the coordinates to the fov_points list
            fov_points[(x_coord, y_coord)] = 0
            # fov_points.append((x_coord, y_coord))
    return fov_points


# if __name__ == '__main__':
#     agent_pos = [328.8917, 301.3598]
#     print(get_fov_points(agent_pos))