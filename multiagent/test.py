import pygame
import random
import math

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

PREDATOR_RADIUS = 20
FOV_RADIUS = 100
WALLS = {  # Dictionary to store walls and their values
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
        fov_points = {}  # Dictionary of FOV points

        for x in range(int(self.predator_x - FOV_RADIUS), int(self.predator_x + FOV_RADIUS)):
            for y in range(int(self.predator_y - FOV_RADIUS), int(self.predator_y + FOV_RADIUS)):
                if x >= 0 and x < SCREEN_WIDTH and y >= 0 and y < SCREEN_HEIGHT:
                    fov_points[(x, y)] = 0  # Set FOV points as 0 (empty space)

        for wall_name, wall_data in WALLS.items():
            for x in range(wall_data['x'], wall_data['x'] + wall_data['width']):
                for y in range(wall_data['y'], wall_data['y'] + wall_data['height']):
                    fov_points[(x, y)] = wall_data['id']  # Set FOV points in walls as the wall's ID

        return fov_points

    # def step(self, action):
    #     self.move_predator(action)
    #     observation = {
    #         'predator_position': [self.predator_x, self.predator_y],
    #         'fov_points': self.get_fov_points(),
    #         'walls': WALLS,
    #     }
    #     reward = 0
    #     done = False
    #     info = {}
    #
    #     fov_points = observation['fov_points']
    #     overlapping_walls = {}  # Dictionary to track overlapping walls
    #
    #     for (x, y), wall_id in fov_points.items():
    #         if wall_id != 0:
    #             if wall_id in overlapping_walls:
    #                 overlapping_walls[wall_id].append((x, y))
    #             else:
    #                 overlapping_walls[wall_id] = [(x, y)]
    #
    #     for wall_id, points in overlapping_walls.items():
    #         wall_name = [name for name, data in WALLS.items() if data['id'] == wall_id][0]
    #         point_str = ', '.join([f"({x}, {y})" for x, y in points])
    #         print(f"FOV overlaps with wall '{wall_name}' at point(s): {point_str}")
    #
    #     return observation, reward, done, info


    # def step(self, action):
    #     self.move_predator(action)
    #     observation = {
    #         'predator_position': [self.predator_x, self.predator_y],
    #         'fov_points': self.get_fov_points(),
    #         'walls': WALLS,
    #     }
    #     reward = 0
    #     done = False
    #     info = {}
    #
    #     fov_points = observation['fov_points']
    #     overlapping_walls = {}  # Dictionary to track overlapping walls
    #
    #     for (x, y), wall_id in fov_points.items():
    #         if wall_id != 0:
    #             if wall_id in overlapping_walls:
    #                 overlapping_walls[wall_id].append((x, y))
    #             else:
    #                 overlapping_walls[wall_id] = [(x, y)]
    #
    #     for wall_id, points in overlapping_walls.items():
    #         wall_name = [name for name, data in WALLS.items() if data['id'] == wall_id][0]
    #         point_str = ', '.join([f"({x}, {y})" for x, y in points])
    #         print(f"FOV overlaps with wall '{wall_name}' at point(s): {point_str}")
    #
    #     return observation, reward, done, info

    def step(self, action):
        self.move_predator(action)
        observation = {
            'predator_position': [self.predator_x, self.predator_y],
            'fov_points': self.get_fov_points(),
            'walls': WALLS,
        }
        reward = 0
        done = False
        info = {}

        fov_points = observation['fov_points']
        overlapping_walls = {}  # Dictionary to track overlapping walls

        for (x, y), wall_id in fov_points.items():
            if wall_id != 0:
                if wall_id in overlapping_walls:
                    overlapping_walls[wall_id].append((x, y))
                else:
                    overlapping_walls[wall_id] = [(x, y)]

        overlaps_str = []

        for wall_id, points in overlapping_walls.items():
            wall_name = [name for name, data in WALLS.items() if data['id'] == wall_id][0]
            x_range = (min(x for x, _ in points), max(x for x, _ in points))
            y_range = (min(y for _, y in points), max(y for _, y in points))
            overlap_str = f"FOV overlaps with wall '{wall_name}' in the range X: {x_range}, Y: {y_range}"
            overlaps_str.append(overlap_str)

        print('\n'.join(overlaps_str))

        return observation, reward, done, info

    def reset(self):
        self.predator_x = SCREEN_WIDTH // 2
        self.predator_y = SCREEN_HEIGHT // 2
        observation = {
            'predator_position': [self.predator_x, self.predator_y],
            'fov_points': self.get_fov_points(),
            'walls': WALLS,
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

    pygame.quit()


if __name__ == "__main__":
    main()
