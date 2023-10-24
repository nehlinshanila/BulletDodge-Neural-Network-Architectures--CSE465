from Agents.fov_points import get_fov_points
import rtree

from Constants.constants import WALLS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


def detect_overlapping_points(agent_position, walls_dict):
    fov_points = get_fov_points(agent_position)
    updated_fov = dict(fov_points)  # Create a copy of the original FOV points
    walls = walls_dict
    # Create an R-tree index to efficiently search for overlapping walls
    idx = rtree.index.Index()
    
    # Insert wall coordinates into the index
    for wall_id, wall_data in walls.items():
        x, y = wall_data['x'], wall_data['y']
        width, height = wall_data['width'], wall_data['height']
        idx.insert(int(wall_id), (x, y, x + width, y + height))

    for fov_point in fov_points:
        x, y = fov_point
        # Check if there's an overlap with any walls using the R-tree index
        if any(idx.intersection((x, y, x, y))):
            updated_fov[fov_point] = 1

    return updated_fov


# if __name__ == '__main__':
#     agent_location = [328.8917, 301.3598]
#     fov_points = get_fov_points(agent_location)
#     updatedfov = detect_overlapping_points(agent_location, WALLS)
#
#     print(updatedfov)
#     Print the FOV points (updatedfov) and their values
#     for point, value in updatedfov.items():
#         print(f"FOV Point: {point}, Value: {value}")
