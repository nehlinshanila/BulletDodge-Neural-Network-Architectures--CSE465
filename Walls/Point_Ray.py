
def is_ray_blocked(agent_pos, goal, walls):
        point_visible = True  # Assume the point is initially visible
        # list 
        ray_start = agent_pos
        x1, y1 = ray_start
        x2, y2 = goal  # Endpoint of the ray is the special point

        for wall in walls:
            wall_vertices = [wall.topleft, wall.topright, wall.bottomright, wall.bottomleft]
            for i in range(len(wall_vertices)):
                x3, y3 = wall_vertices[i]
                x4, y4 = wall_vertices[(i + 1) % len(wall_vertices)]

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
