import math
from Constants.constants import FOV_RADIUS, WALLS
# Constants


def get_fov_rays(agent_position):
    fov_rays = []
    x, y = agent_position

    for angle in range(0, 360, 5):  # Cast rays every 5 degrees
        radians = math.radians(angle)
        dx = math.cos(radians)
        dy = math.sin(radians)
        obs_id = 0  # Default id if ray doesn't intersect with any screen
        remaining_distance = FOV_RADIUS

        for r in range(1, FOV_RADIUS + 1):
            ray_x = int(x + r * dx)
            ray_y = int(y + r * dy)

            for obs_name, data in WALLS.items():
                if data['check'](ray_x, ray_y):
                    obs_id = data.get('id', 0)  # Add a default 'id' value if it's present in the 'data' dictionary
                    remaining_distance = min(remaining_distance, r)
                    break
        fov_rays.append([angle, remaining_distance, obs_id])

    return fov_rays


if __name__ == '__main__':
    agent_pos = [300, 300]

    print(get_fov_rays(agent_pos))
