import math
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Constants.constants import FOV_RADIUS, WALLS
# Constants


        # Define objects with arbitrary shapes
        self.objects = {
            "wall2": [(200, 300), (220, 300), (220, 400), (200, 400)],
            "wall3": [(300, 200), (320, 200), (320, 300), (300, 300)],
            "wall4": [(400, 400), (430, 400), (430, 430), (400, 430)]
        }

    def is_ray_blocked(self, ray_start, ray_angle):
        point_visible = True  # Assume the point is initially visible

        x1, y1 = ray_start
        x2, y2 = self.special_point  # Endpoint of the ray is the special point

        for object_name, object_vertices in self.objects.items():
            for i in range(len(object_vertices)):
                x3, y3 = object_vertices[i]
                x4, y4 = object_vertices[(i + 1) % len(object_vertices)]

                denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

                if denominator == 0:
                    continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

                epsilon = 1e-5  # Small epsilon value
                if -epsilon <= t <= 1 + epsilon and 0 <= u <= 1:
                    point_visible = False
                    break

        return point_visible

if __name__ == '__main__':
    agent_pos = [300, 300]

    print(get_fov_rays(agent_pos))
