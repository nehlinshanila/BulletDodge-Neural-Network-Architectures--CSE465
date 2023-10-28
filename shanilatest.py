import pygame
import sys
import math

class GameEnv:
    def __init__(self, width, height):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Predator Agent Environment")

        # Define colors
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Predator agent position and size
        self.predator_x, self.predator_y = self.WIDTH // 2, self.HEIGHT // 2
        self.predator_radius = 10
        self.move_step = 1

        self.special_point = (100, 100)  # Single point at (100, 100)
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

    def render(self):
        self.screen.fill(self.WHITE)

        ray_start = (self.predator_x, self.predator_y)
        ray_angle = math.degrees(math.atan2(self.special_point[1] - self.predator_y, self.special_point[0] - self.predator_x))

        # Draw the dynamic ray
        ray_end_x = self.special_point[0]
        ray_end_y = self.special_point[1]
        ray_obstructed = self.is_ray_blocked(ray_start, ray_angle)
    
        if ray_obstructed:
            pygame.draw.line(self.screen, self.RED, ray_start, (ray_end_x, ray_end_y), 1)

        # Draw the special point
        pygame.draw.circle(self.screen, self.RED, self.special_point, 5)

        for object_name, object_vertices in self.objects.items():
            pygame.draw.polygon(self.screen, self.GREEN, object_vertices)

        # Draw the predator agent
        pygame.draw.circle(self.screen, self.RED, (self.predator_x, self.predator_y), self.predator_radius)

        pygame.display.flip()



    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.predator_x -= self.move_step
            if keys[pygame.K_RIGHT]:
                self.predator_x += self.move_step
            if keys[pygame.K_UP]:
                self.predator_y -= self.move_step
            if keys[pygame.K_DOWN]:
                self.predator_y += self.move_step

            self.render()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameEnv(800, 600)
    game.run()
