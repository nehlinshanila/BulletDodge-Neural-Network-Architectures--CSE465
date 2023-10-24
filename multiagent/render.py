# import pygame
# import random

# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)

# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 600
# PREDATOR_RADIUS = 20

# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# class GameEnv:
#     def __init__(self):
#         self.predator_x = SCREEN_WIDTH // 2
#         self.predator_y = SCREEN_HEIGHT // 2

#         # Wall properties
#         self.walls = [
#             {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 250},
#             {'x': SCREEN_WIDTH // 2 - 25, 'y': 350, 'width': 50, 'height': 250},
#         ]

#     def move_predator(self, action):
#         if action == 0:  # Move up
#             self.predator_y -= 2
#         elif action == 1:  # Move down
#             self.predator_y += 2
#         elif action == 2:  # Move left
#             self.predator_x -= 2
#         elif action == 3:  # Move right
#             self.predator_x += 2

#         self.predator_x = max(PREDATOR_RADIUS, min(SCREEN_WIDTH - PREDATOR_RADIUS, self.predator_x))
#         self.predator_y = max(PREDATOR_RADIUS, min(SCREEN_HEIGHT - PREDATOR_RADIUS, self.predator_y))

#     def render(self):
#         for wall in self.walls:
#             pygame.draw.rect(screen, BLUE, (wall['x'], wall['y'], wall['width'], wall['height']))
#         pygame.draw.circle(screen, RED, (int(self.predator_x), int(self.predator_y)), PREDATOR_RADIUS)

#     def step(self, action):
#         self.move_predator(action)
#         return self.predator_x, self.predator_y

# def main():
#     env = GameEnv()
#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         action = random.choice([0, 1, 2, 3])
#         predator_x, predator_y = env.step(action)

#         screen.fill(WHITE)
#         env.render()

#         pygame.display.flip()

#     pygame.quit()

# if __name__ == "__main__":
#     main()


import pygame
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PREDATOR_RADIUS = 20

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
        wall1 = {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 250}
        wall2 = {'x': SCREEN_WIDTH // 2 - 25, 'y': 350, 'width': 50, 'height': 250}

        pygame.draw.rect(screen, BLUE, (wall1['x'], wall1['y'], wall1['width'], wall1['height']))
        pygame.draw.rect(screen, BLUE, (wall2['x'], wall2['y'], wall2['width'], wall2['height']))
        pygame.draw.circle(screen, RED, (int(self.predator_x), int(self.predator_y)), PREDATOR_RADIUS)

    def step(self, action):
        self.move_predator(action)
        return self.predator_x, self.predator_y

def main():
    env = GameEnv()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = random.choice([0, 1, 2, 3])
        predator_x, predator_y = env.step(action)

        screen.fill(WHITE)
        env.render()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
