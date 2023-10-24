from fov_points import get_fov_points
from constants import WALLS, SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS

import rtree

def detect_overlapping_points(agent_position, walls):
    fov_points = get_fov_points(agent_position)
    updatedfov = dict(fov_points)  # Create a copy of the original FOV points

    # Create an R-tree index to efficiently search for overlapping walls
    idx = rtree.index.Index()
    
    # Insert wall coordinates into the index
    for wall_id, wall_data in walls.items():
        x, y = wall_data['x'], wall_data['y']
        width, height = wall_data['width'], wall_data['height']
        idx.insert(wall_id, (x, y, x + width, y + height))

    for fov_point, value in fov_points.items():
        x, y = fov_point
        # Check if there's an overlap with any walls using the R-tree index
        if any(idx.intersection((x, y, x, y))):
            updatedfov[fov_point] = 1

    return updatedfov

if __name__ == '__main':
    agent_location = [328.8917, 301.3598]
    fov_points = get_fov_points(agent_location)
    updatedfov = detect_overlapping_points(agent_location, WALLS)

    # Print the FOV points (updatedfov) and their values
    for point, value in updatedfov.items():
        print(f"FOV Point: {point}, Value: {value}")

