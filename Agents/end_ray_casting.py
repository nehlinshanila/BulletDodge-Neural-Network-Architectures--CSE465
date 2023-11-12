import math
import numpy as np

def get_cast_ray_angles(agent_angle):
    start_angle = agent_angle - 65  # 65 degrees to the left
    end_angle = agent_angle + 65  # 65 degrees to the right
    angle_step = 10  # One ray every 10 degrees
    ray_angles = np.arange(start_angle, end_angle + angle_step, angle_step).tolist()
    ray_angles = [angle%360 for angle in ray_angles]

    return ray_angles

def is_ray_blocked(agent, wall_list):
    
    ray_angles = get_cast_ray_angles(agent.angle)
    ray_lengths = []
    
    for ray_angle in ray_angles:
        x1, y1 = agent.center
        x2, y2 = x1 + 1000 * math.cos(math.radians(ray_angle)), y1 + 1000 * math.sin(math.radians(ray_angle))
        lengths = None

        for wall in wall_list:
            x3, y3 = wall.x, wall.y
            x4, y4 = wall.topright[0], wall.bottomright[1]

            for side in [(x3, y3, x4, y3), (x4, y3, x4, y4), (x4, y4, x3, y4), (x3, y4, x3, y3)]:
                x5, y5, x6, y6 = side

                denominator = (x1 - x2) * (y5 - y6) - (y1 - y2) * (x5 - x6)

                if denominator == 0:
                    continue

                t = ((x1 - x5) * (y5 - y6) - (y1 - y5) * (x5 - x6)) / denominator
                u = -((x1 - x2) * (y1 - y5) - (y1 - y2) * (x1 - x5)) / denominator

                epsilon = 1e-5  # Small epsilon value

                if 0 <= t <= 1 and 0 <= u <= 1:
                    intersection_x = x1 + t * (x2 - x1)
                    intersection_y = y1 + t * (y2 - y1)

                    # Calculate the distance from the ray start to the intersection point
                    distance = math.sqrt((intersection_x - x1) ** 2 + (intersection_y - y1) ** 2)

                    if lengths is None or distance < lengths:
                        lengths = distance
              
        if lengths is None:
            lengths = 1000
            
        ray_lengths.append(lengths)
    return ray_lengths, ray_angles
