import numpy as np

from constants import SCREEN_HEIGHT,SCREEN_WIDTH,FOV_RADIUS

#! time complexity of O(n)
def get_fov_points(agent_position):
    fov_points = []
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
            fov_points.append((x_coord, y_coord))
    return fov_points

#?print
# if __name__ == '__main__':
#     agent_location = [328.8917, 301.3598]
#     print(get_fov_points(agent_location))

# def get_fov_points(agent_position):
#         fov_points = {}  # Dictionary to store FOV points within the agent's FOV
#         # variables define the range of coordinates(x,y) relative to the agent's position within the FOV
#         fov_x = range(int(-FOV_RADIUS), int(FOV_RADIUS))
#         fov_y = range(int(-FOV_RADIUS), int(FOV_RADIUS))
#         # Iterate over FOV coordinates
#         for x in fov_x:
#             for y in fov_y:
#                 fov_x_coord = int(agent_position[0] + x)
#                 fov_y_coord = int(agent_position[1] + y)
#                 # checks whether the calculated coordinates fall within the agent's FOV and the screen boundaries.
#                 if 0 <= fov_x_coord < SCREEN_WIDTH and 0 <= fov_y_coord < SCREEN_HEIGHT:
#                     # If the coordinates are within the FOV and screen boundaries, the point
#                     # is added to the fov_points dictionary with a value of 0, indicating an assumption of empty space.
#                     fov_points[(fov_x_coord, fov_y_coord)] = 0
#         return fov_points

# def get_fov_points(agent_position):
#     fov_points = {}
#     # NumPy array x_range that represents a range of X and Y coordinates within the FOV radius.
#     x_range = np.arange(agent_position[0] - FOV_RADIUS, agent_position[0] + FOV_RADIUS)
#     y_range = np.arange(agent_position[1] - FOV_RADIUS, agent_position[1] + FOV_RADIUS)
#     # NumPy's meshgrid function to create 2D arrays xv and yv where xv == X coordinates and yv == Y coordinates
#     xv, yv = np.meshgrid(x_range, y_range)
#     # Calculate Euclidean distances of each point (X, Y) from the agent's position (agent_position[0], agent_position[1]) 
#     # using the Pythagorean theorem. This results in the distances array, where each element is the distance from the agent.
#     distances = np.sqrt((xv - agent_position[0])**2 + (yv - agent_position[1])**2)
#     # Check if points are within FOV and screen boundaries by seeing if distance is less than or equal to the FOV radius.
#     valid_points = (distances <= FOV_RADIUS) & (xv >= 0) & (xv < SCREEN_WIDTH) & (yv >= 0) & (yv < SCREEN_HEIGHT)
#     # Get the coordinates of valid points
#     x_coords, y_coords = xv[valid_points], yv[valid_points]
#     # Create a dictionary of FOV points
#     fov_points = {(int(x), int(y)): 0 for x, y in zip(x_coords.ravel(), y_coords.ravel())}
    
#     return fov_points

# if __name__ == '__main__':
#     agent_location = [328.8917, 301.3598]
#     print(get_fov_points(agent_location))

#! time complexity of O(n)
# def get_fov_points(agent_position):
#     fov_points = {}
#     x, y = agent_position
#     #loop that iterates from 0 to 359, representing all possible angles in degrees.
#     for angle in range(360):
#         # Convert angle to radians
#         radians = np.deg2rad(angle)
#         # Calculate new coordinates within FOV based on polar coordinates 
#         x_coord = int(x + FOV_RADIUS * np.cos(radians))
#         y_coord = int(y + FOV_RADIUS * np.sin(radians))
#         # checks if the calculated x_coord and y_coord fall within the screen boundaries.
#         if 0 <= x_coord < SCREEN_WIDTH and 0 <= y_coord < SCREEN_HEIGHT:
#             # if yes then == 0 or empty space
#             fov_points[(x_coord, y_coord)] = 0
#     return fov_points

# if __name__ == '__main__':
#     agent_location = [328.8917, 301.3598]
#     print(get_fov_points(agent_location))

