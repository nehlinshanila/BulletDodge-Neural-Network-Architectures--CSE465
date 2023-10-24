import os
import sys
# data structure like a 2D range tree, which can help speed up range searching using library
from sortedcontainers import SortedDict

from Agents.fov_points import get_fov_points
# from .Constants.constants import WALLS, FOV_RADIUS
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# ! time complexity is O(n log n)
# Creating the SortedDict: O(n log n)
# Iterating through the FOV points: O(n)
# Finding overlapping x-ranges: O(log n)
# Determining which walls are overlapping: O(1)
# Since the function iterates through the FOV points, the overall time complexity is O(n log n).
def detect_overlapping_points(agent_position, walls, fov_radius):
    fov_points = get_fov_points(agent_position)
    overlapping_walls = {}

    # Create a SortedDict to efficiently query wall x-ranges
    wall_x_ranges = SortedDict()
    # Initialize a dictionary to track wall IDs
    wall_ids = {}

    # Iterate through the walls
    for wall_id, wall_data in walls.items():
        x_wall, y_wall = wall_data['x'], wall_data['y']
        width, height = wall_data['width'], wall_data['height']
        # Store the wall's x-range in the sorted dictionary
        wall_x_ranges[x_wall] = x_wall + width
        # Create a mapping from x-range to wall ID for efficient lookup
        wall_ids[x_wall] = wall_id

    # Iterate through the FOV points
    for fov_point in fov_points:
        x_fov, y_fov = fov_point
        # Use the i_range method to find wall x-ranges overlapping with the FOV point
        overlapping_x_ranges = wall_x_ranges.irange(x_fov - fov_radius, x_fov + fov_radius)
        # Iterate through the overlapping x-ranges and determine which walls are overlapping
        for x_range in overlapping_x_ranges:
            wall_id = wall_ids[x_range]
            if wall_id in overlapping_walls:
                overlapping_walls[wall_id].append(fov_point)
            else:
                overlapping_walls[wall_id] = [fov_point]

    return overlapping_walls

