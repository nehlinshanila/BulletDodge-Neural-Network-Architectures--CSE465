from Agents.RayCasting_Walls import calculate_wall_intersection

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FOV_RADIUS = 100
PREDATOR_RADIUS = 20


WALLS = {
    'top': {
        'id': 11,
        'check': lambda ray_x, ray_y: ray_y < 0,
    },
    'right': {
        'id': 22,
        'check': lambda ray_x, ray_y: ray_x >= SCREEN_WIDTH,
    },
    'left': {
        'id': 33,
        'check': lambda ray_x, ray_y: ray_x < 0,
    },
    'bottom': {
        'id': 44,
        'check': lambda ray_x, ray_y: ray_y >= SCREEN_HEIGHT,
    },
    'wall1': {
        'id': 1,    #WALLS2: id = 1
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 2 - 25 <= ray_x <= SCREEN_WIDTH // 2 + 25 and 0 <= ray_y <= 250,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 2 - 25, 0, SCREEN_WIDTH // 2 + 25, 250)
    },
    'wall2': {
        'id': 2,    #WALLS2: id = 2
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 2 - 25 <= ray_x <= SCREEN_WIDTH // 2 + 25 and 350 <= ray_y <= 600,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 2 - 25, 350, SCREEN_WIDTH // 2 + 25, 600)
    },
    'wall3': {
        'id': 3,    #WALLS2: id = 3
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 4 - 25 <= ray_x <= SCREEN_WIDTH // 4 + 25 and 0 <= ray_y <= 450,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 4 - 25, 0, SCREEN_WIDTH // 4 + 25, 450)
    },
    'wall4': {
        'id': 4,    #WALLS2: id = 4
        'check': lambda ray_x, ray_y: SCREEN_WIDTH // 4 - 25 <= ray_x <= SCREEN_WIDTH // 4 + 25 and 550 <= ray_y <= 600,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, SCREEN_WIDTH // 4 - 25, 550, SCREEN_WIDTH // 4 + 25, 600)
    },
    'wall5': {
        'id': 5,    #WALLS2: id = 5
        'check': lambda ray_x, ray_y: (3 * SCREEN_WIDTH) // 4 - 25 <= ray_x <= (3 * SCREEN_WIDTH) // 4 + 25 and 0 <= ray_y <= 250,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, (3 * SCREEN_WIDTH) // 4 - 25, 0, (3 * SCREEN_WIDTH) // 4 + 25, 250)
    },
    'wall6': {
        'id': 6,   #WALLS2: id = 6
        'check': lambda ray_x, ray_y: (3 * SCREEN_WIDTH) // 4 - 25 <= ray_x <= (3 * SCREEN_WIDTH) // 4 + 25 and 350 <= ray_y <= 600,
        'calc': lambda x, y, dx, dy: calculate_wall_intersection(x, y, dx, dy, (3 * SCREEN_WIDTH) // 4 - 25, 350, (3 * SCREEN_WIDTH) // 4 + 25, 600)
    }
}

# WALLS2 = {
#     '1': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 50},
#     '2': {'x': SCREEN_WIDTH // 2 - 25, 'y': 150, 'width': 50, 'height': 450},
#     '3': {'x': SCREEN_WIDTH // 4 - 25, 'y': 0, 'width': 50, 'height': 450},
#     '4': {'x': SCREEN_WIDTH // 4 - 25, 'y': 550, 'width': 50, 'height': 50},
#     '5': {'x': (3 * SCREEN_WIDTH) // 4 - 25, 'y': 0, 'width': 50, 'height': 250},
#     '6': {'x': (3 * SCREEN_WIDTH) // 4 - 25, 'y': 350, 'width': 50, 'height': 250},
# }

LEVEL_1_WALLS = {
    '1': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 50},
    '2': {'x': SCREEN_WIDTH // 2 - 25, 'y': 150, 'width': 50, 'height': 450},
}

LEVEL_2_WALLS = {
    '1': {'x': SCREEN_WIDTH // 4 - 25, 'y': 0, 'width': 50, 'height': 450},
    '2': {'x': SCREEN_WIDTH // 4 - 25, 'y': 550, 'width': 50, 'height': 50},
    '3': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 50},
    '4': {'x': SCREEN_WIDTH // 2 - 25, 'y': 150, 'width': 50, 'height': 450},
}

LEVEL_3_WALLS = {
    '1': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 50},
    '2': {'x': SCREEN_WIDTH // 2 - 25, 'y': 150, 'width': 50, 'height': 450},
    '3': {'x': SCREEN_WIDTH // 4 - 25, 'y': 0, 'width': 50, 'height': 450},
    '4': {'x': SCREEN_WIDTH // 4 - 25, 'y': 550, 'width': 50, 'height': 50},
    '5': {'x': (3 * SCREEN_WIDTH) // 4 - 25, 'y': 0, 'width': 50, 'height': 250},
    '6': {'x': (3 * SCREEN_WIDTH) // 4 - 25, 'y': 350, 'width': 50, 'height': 250},
}

#level_1_walls, level_2_walls
