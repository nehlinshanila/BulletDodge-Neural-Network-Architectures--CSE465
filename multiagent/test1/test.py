import pygame
import random
import math
import numpy as np


from fov_points import get_fov_points
from overlap_detection import detect_overlapping_points
from constants import WHITE, RED, BLUE, GREEN, FOV_RADIUS, PREDATOR_RADIUS, WALLS, SCREEN_WIDTH, SCREEN_HEIGHT


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

    def render(self):
        screen.fill(WHITE)  # Clear the screen

        for wall in [WALLS['wall4'], WALLS['wall5']]:
            pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))

        pygame.draw.circle(screen, RED, (int(self.predator_x), int(self.predator_y)), PREDATOR_RADIUS)

        pygame.display.flip()  # Update the display



    
    def step(self, action):
        self.move_predator(action)
    # returning the following ===
        # predator initial positions
        # dictionary containing information about the points within the predator's field of view (FOV).
        # dictionary containing information about the walls in the environment.
        # dictionary containing information about which walls overlap with the predator's FOV.
        observation = {
            'predator_position': [self.predator_x, self.predator_y],
            'fov_points':get_fov_points([self.predator_x, self.predator_y]),
            'walls': WALLS,
            'overlapping_walls': detect_overlapping_points([self.predator_x, self.predator_y], WALLS),
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
            'fov_points': get_fov_points([self.predator_x, self.predator_y]),
            'walls': WALLS,
            'overlapping_walls': detect_overlapping_points([self.predator_x, self.predator_y]),
        }
        return observation


def main():
    env = GameEnv()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # actionspace.sample
        action = random.choice([0, 1, 2, 3])
        observation, reward, done, info = env.step(action)

        screen.fill(WHITE)
        env.render()


        # Print FOV overlapped points
        # overlapping_walls = observation['overlapping_walls']
        # str = " "
        # for wall_id, overlaps in overlapping_walls.items():
        #     for coord in overlaps:
        #         str += f"FOV overlaps with wall ID {wall_id} at coordinates: {coord}\n"
        #     print(str)
        
         # The following part for detecting overlapping walls and printing information should be placed here
        agent_position = [env.predator_x, env.predator_y]
        overlapping_walls = detect_overlapping_points(agent_position, WALLS)

        # for wall_id, coordinates in overlapping_walls.items():
        #     wall_name = f'Wall {wall_id}'
        #     print(wall_name, "is overlapping with the agent's FOV at the following coordinates:")
        #     for coord in coordinates:
        #         x_coord, y_coord = coord
        #         print(f"Coordinates: ({x_coord}, {y_coord})")
        for wall_id, coordinates in overlapping_walls.items():
            wall_name = f'Wall {wall_id}'
            coordinates_str = ", ".join([f'({x_coord}, {y_coord})' for x_coord, y_coord in coordinates])
            print(f"FOV is overlapping with {wall_name}: {coordinates_str}")

        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    main()


# fov radius lower for fog