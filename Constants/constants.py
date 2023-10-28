from Agents.RayCasting_Walls import calculate_wall_intersection

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

FOV_RADIUS = 100
PREDATOR_RADIUS = 20
special_point = (100, 100)  # Custom end point for agent in game
WALLS = {
    'top': {
        'id': 1,
        'check': lambda ray_x, ray_y: ray_y < 0,
    },
    'right': {
        'id': 2,
        'check': lambda ray_x, ray_y: ray_x >= SCREEN_WIDTH,
    },
    'left': {
        'id': 4,
        'check': lambda ray_x, ray_y: ray_x < 0,
    },
    'bottom': {
        'id': 3,
        'check': lambda ray_x, ray_y: ray_y >= SCREEN_HEIGHT,
    },
    'wall1': {
        'id': 6,
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 2 - 25 <= ray_x <= SCREEN_WIDTH // 2 + 25 and 0 <= ray_y <= 250,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 2 - 25, 0, SCREEN_WIDTH // 2 + 25, 250)
    },
    'wall2': {
        'id': 7,
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 2 - 25 <= ray_x <= SCREEN_WIDTH // 2 + 25 and 350 <= ray_y <= 600,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 2 - 25, 350, SCREEN_WIDTH // 2 + 25, 600)
    }
}

WALLS2 = {
    '1': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 250},
    '2': {'x': SCREEN_WIDTH // 2 - 25, 'y': 350, 'width': 50, 'height': 250}
}