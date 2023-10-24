"""
this part is only to handle the wall buildings and destruction when necessary

we've used pygame.Rect function to build the wall rectangles
"""


class Walls:
    def __init__(self, pygame):
        self.pygame = pygame
        self.walls = []

    # takes a dictionary of walls and creates objects of pygame.Rect()
    # the dictionary of walls needs to contain the x, y, width, height of the walls
    # any extra key:value are unused or maybe used if needed in the future
    def make_wall(self, wall_list):
        for key, value in wall_list.items():
            x = value['x']
            y = value['y']
            width = value['width']
            height = value['height']
            wall = self.pygame.Rect(x, y, width, height)
            self.walls.append(wall)

        return self.walls

    # destroys all the existing wall objects inside the walls list
    def clear_walls(self):
        self.walls = []
