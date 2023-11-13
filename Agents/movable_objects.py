import math
import pygame
import numpy as np
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Walls.wall_class import Walls
from Agents.agent import Agent

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Casting Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create an instance of the Agent class
predator_agent = Agent("Predator", 1)
predator_agent.agent_reset(WIDTH, HEIGHT)

# Define walls with new format
LEVEL_5_WALLS = {
    "1": {"x": 150, "y": 120, "width": 100, "height": 30},
    "2": {"x": 300, "y": 80, "width": 30, "height": 60},
    "3": {"x": 450, "y": 120, "width": 100, "height": 30},
    "4": {"x": 600, "y": 180, "width": 30, "height": 100},
    "5": {"x": 500, "y": 400, "width": 100, "height": 30},
    "6": {"x": 150, "y": 250, "width": 30, "height": 200},
    "7": {"x": 300, "y": 500, "width": 150, "height": 30}
}

wall_object = Walls(pygame)
walls = wall_object.make_wall(LEVEL_5_WALLS)

def get_cast_ray_angles(agent_angle):
    start_angle = agent_angle - 65  # 65 degrees to the left
    end_angle = agent_angle + 65  # 65 degrees to the right
    angle_step = 10  # One ray every 10 degrees
    ray_angles = np.arange(start_angle, end_angle + angle_step, angle_step).tolist()
    ray_angles = [angle % 360 for angle in ray_angles]

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

class MovableObject:
    def __init__(self, object_id, position, radius):
        self.object_id = object_id
        self.position = np.array(position, dtype=np.float32)
        self.radius = radius

# Create a list for movable objects
movable_objects = [MovableObject(1, [200, 300], 15), MovableObject(2, [400, 200], 20)]

def move_agent_and_objects(agent, movable_objects, walls, keys):
    # Store the agent's previous position
    agent.previous_position = np.copy(agent.current_position)

    # Update agent's rotation based on arrow key inputs
    if keys[pygame.K_LEFT]:
        agent.step_update(action=1, speed_factor=0.022, range_x=WIDTH, range_y=HEIGHT)
    if keys[pygame.K_RIGHT]:
        agent.step_update(action=0, speed_factor=0.022, range_x=WIDTH, range_y=HEIGHT)
    if keys[pygame.K_UP]:
        agent.step_update(2, 0.022, WIDTH, HEIGHT)

    # Check for collision with movable objects
    hit_object = get_hit_movable_object(agent, movable_objects)

    if hit_object is not None:
        # Move only the hit movable object based on agent's movement
        hit_object.position += agent.current_position - agent.previous_position

    return agent.current_position


def get_hit_movable_object(agent, movable_objects):
    print(f"Agent Position: {agent.current_position}")
    for obj in movable_objects:
        obj_position = obj.position
        obj_radius = obj.radius

        distance_to_obj = np.linalg.norm(agent.current_position - obj_position)
        print(f"Object {obj.object_id} Position: {obj_position}, Distance to Object: {distance_to_obj}")

        if distance_to_obj < obj_radius:
            print(f"Hit object with ID {obj.object_id}")
            return obj  # Return the object if hit

    print("No object hit")
    return None  # Return None if no object is hit


def update_agent_position(agent, hit_object):
    if hit_object is not None:
        # Update the position of the movable object based on agent's movement
        hit_object.position += agent.current_position - agent.previous_position
        # Update the agent's position based on the collision
        agent.current_position = hit_object.position + (agent.current_position - agent.previous_position)

# Pygame main loop
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        agent_position = move_agent_and_objects(predator_agent, movable_objects, walls, keys)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the agent
        pygame.draw.circle(screen, RED, predator_agent.center, 10)

        # Draw movable objects
        for obj in movable_objects:
            pygame.draw.circle(screen, BLUE, obj.position.astype(int), obj.radius)

        lengths, angles = is_ray_blocked(predator_agent, walls)
        for length, angle in zip(lengths, angles):
            if length < 1000:
                color = RED
            else:
                color = BLUE
            # Draw the ray with the calculated length
            ray_end_x = predator_agent.center[0] + length * np.cos(np.radians(angle))
            ray_end_y = predator_agent.center[1] + length * np.sin(np.radians(angle))
            start_pos = predator_agent.center
            end_pos = (int(ray_end_x), int(ray_end_y))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)

        # Render the walls
        for wall_data in LEVEL_5_WALLS.values():
            pygame.draw.rect(screen, BLACK, (wall_data["x"], wall_data["y"], wall_data["width"], wall_data["height"]))

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 frames per second

if __name__ == "__main__":
    main()
