import pygame
import random
import math

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

PREDATOR_RADIUS = 20
FOV_RADIUS = 100
WALLS = {
    'wall1': {'x': 280, 'y': 200, 'width': 20, 'height': 40, 'id': 1},
    'wall2': {'x': 320, 'y': 190, 'width': 30, 'height': 60, 'id': 2},
    'wall3': {'x': 390, 'y': 250, 'width': 25, 'height': 30, 'id': 3}
}

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class GameEnv:
    def __init__(self):
        self.predator_x = SCREEN_WIDTH // 2
        self.predator_y = SCREEN_HEIGHT // 2

    def move_predator(self, action):
        if action == 0:  # Move up
            self.predator_y -= 2
        elif action == 1:  # Move down
            self.predator_y += 2
        elif action == 2:  # Move left
            self.predator_x -= 2
        elif action == 3:  # Move right
            self.predator_x += 2

        self.predator_x = max(PREDATOR_RADIUS, min(SCREEN_WIDTH - PREDATOR_RADIUS, self.predator_x))
        self.predator_y = max(PREDATOR_RADIUS, min(SCREEN_HEIGHT - PREDATOR_RADIUS, self.predator_y))

    def draw_environment(self):
        for wall in WALLS.values():
            pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))
        pygame.draw.circle(screen, RED, (int(self.predator_x), int(self.predator_y)), PREDATOR_RADIUS)
        pygame.draw.circle(screen, BLUE, (int(self.predator_x), int(self.predator_y)), FOV_RADIUS, 1)

    def get_fov_points(self):
        fov_points = {}  # Dictionary to store FOV points within the agent's FOV
        # variables define the range of coordinates(x,y) relative to the agent's position within the FOV
        fov_x = range(int(-FOV_RADIUS), int(FOV_RADIUS))
        fov_y = range(int(-FOV_RADIUS), int(FOV_RADIUS))
        # Iterate over FOV coordinates
        for x in fov_x:
            for y in fov_y:
                fov_x_coord = int(self.predator_x + x)
                fov_y_coord = int(self.predator_y + y)
                # checks whether the calculated coordinates fall within the agent's FOV and the screen boundaries.
                if 0 <= fov_x_coord < SCREEN_WIDTH and 0 <= fov_y_coord < SCREEN_HEIGHT:
                    # If the coordinates are within the FOV and screen boundaries, the point
                    # is added to the fov_points dictionary with a value of 0, indicating an assumption of empty space.
                    fov_points[(fov_x_coord, fov_y_coord)] = 0
        return fov_points

    def detect_overlapping_points(self):
        fov_points = self.get_fov_points()
        overlapping_walls = {}  # Dictionary to track overlapping walls
        # iterates over the coordinates within the agent's FOV.
        for fov_x_coord, fov_y_coord in fov_points.keys():
            # iterates over the walls in the environment in the WALLS dictionary.
            for wall_name, wall_data in WALLS.items():
                # variables define the x,y coordinates that belong
                # to a certain wall based on its position and dimensions.
                wall_x_range = range(wall_data['x'], wall_data['x'] + wall_data['width'])
                wall_y_range = range(wall_data['y'], wall_data['y'] + wall_data['height'])
                # checks whether the current FOV point is inside the range of
                # coordinates for the current wall. If it is, it indicates an overlap.
                if fov_x_coord in wall_x_range and fov_y_coord in wall_y_range:
                    wall_id = wall_data['id']
                    if wall_id in overlapping_walls:
                        overlapping_walls[wall_id].append((fov_x_coord, fov_y_coord))
                    else:
                        overlapping_walls[wall_id] = [(fov_x_coord, fov_y_coord)]
        # If an overlap is detected, the code adds its id to the overlapping_walls dictionary.
        return overlapping_walls

    def step(self, action):
        self.move_predator(action)
    # returning the following ===
        # predator initial positions
        # dictionary containing information about the points within the predator's field of view (FOV).
        # dictionary containing information about the walls in the environment.
        # dictionary containing information about which walls overlap with the predator's FOV.
        observation = {
            'predator_position': [self.predator_x, self.predator_y],
            'fov_points': self.get_fov_points(),
            'walls': WALLS,
            'overlapping_walls': self.detect_overlapping_points(),
        }
        reward = 0
        done = False
        info = {}

        return observation, reward, done, info

    def reset(self):
        self.predator_x = SCREEN_WIDTH // 2
        self.predator_y = SCREEN_HEIGHT // 2
        observation = {
            'predator_position': [self.predator_x, self.predator_y],
            'fov_points': self.get_fov_points(),
            'walls': WALLS,
            'overlapping_walls': self.detect_overlapping_points(),
        }
        return observation


def main():
    env = GameEnv()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = random.choice([0, 1, 2, 3])
        observation, reward, done, info = env.step(action)

        screen.fill(WHITE)
        env.draw_environment()

        pygame.display.flip()

        # Print FOV overlapped points
        overlapping_walls = observation['overlapping_walls']
        for wall_id, overlaps in overlapping_walls.items():
            for coord in overlaps:
                print(f"FOV overlaps with wall ID {wall_id} at coordinates: {coord}")

    pygame.quit()


if __name__ == "__main__":
    main()
