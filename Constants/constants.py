
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FOV_RADIUS = 100
PREDATOR_RADIUS = 20


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


#main complicated wall

# LEVEL_7_WALLS = {
#     '7': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 120},  #top vertical wall
#     '8': {'x': SCREEN_WIDTH // 2 - 25, 'y': 220, 'width': 50, 'height': 240}, #middle vertical wall
#     '9': {'x': SCREEN_WIDTH // 2 - 25, 'y': 560, 'width': 50, 'height': 40},  #bottom vertical wall
#     '10': {'x': 0, 'y': 300, 'width': 150, 'height': 50}, #horizontal wall on left
#     '11': {'x': SCREEN_WIDTH // 4 + 50, 'y': 300, 'width': 125, 'height': 50}, ##horizontal wall on left
#     '12': {'x': SCREEN_WIDTH // 2 + 25, 'y': 380, 'width': 150, 'height': 50}, #horizontal wall on right
#     '13': {'x': SCREEN_WIDTH - 105, 'y': 380, 'width': 110, 'height': 50}, #horizontal wall on right  
# }

LEVEL_4_WALLS = {
        '1': {'x': SCREEN_WIDTH // 2 - 25, 'y': 0, 'width': 50, 'height': 120, 'name': 'obs_w', 'gate_with' : 2, 'access' : 'left_right', 'orientation' : 'vertical'},  
        '2': {'x': SCREEN_WIDTH // 2 - 25, 'y': 220, 'width': 50, 'height': 240, 'name': 'obs_w', 'gate_with' : 1, 'access' : 'left_right', 'orientation' : 'vertical'}, 
        '3': {'x': SCREEN_WIDTH // 2 - 25, 'y': 560, 'width': 50, 'height': 40, 'name': 'obs_w', 'gate_with' : 2, 'access' : 'left_right', 'orientation' : 'vertical'},  
        '4': {'x': 0, 'y': 300, 'width': 150, 'height': 50, 'name': 'obs_w', 'gate_with' : 5, 'access' : 'bottom_top', 'orientation' : 'horizontal'},
        '5': {'x': SCREEN_WIDTH // 4 + 50, 'y': 300, 'width': 125, 'height': 50, 'name': 'obs_w', 'gate_with' : 4, 'access' : 'bottom_top', 'orientation' : 'horizontal'}, 
        '6': {'x': SCREEN_WIDTH // 2 + 25, 'y': 380, 'width': 150, 'height': 50, 'name': 'obs_w', 'gate_with' : 7, 'access' : 'bottom_top', 'orientation' : 'horizontal'}, 
        '7': {'x': SCREEN_WIDTH - 105, 'y': 380, 'width': 110, 'height': 50, 'name': 'obs_w', 'gate_with' : 6, 'access' : 'bottom_top', 'orientation' : 'horizontal'}, 
    
}


# LEVEL_5_WALLS = {
#     '1': {'x1': 200, 'y1': 0, 'x2': 200, 'y2': 150, 'name': 'obs_w', 'orientation': 'diagonal'},
#     '2': {'x1': 200, 'y1': 150, 'x2': 400, 'y2': 150, 'name': 'obs_w', 'orientation': 'diagonal'},
#     '3': {'x1': 400, 'y1': 150, 'x2': 400, 'y2': 0, 'name': 'obs_w', 'orientation': 'diagonal'},
#     '4': {'x1': 400, 'y1': 0, 'x2': 200, 'y2': 0, 'name': 'obs_w', 'orientation': 'diagonal'},
#     '5': {'x1': 250, 'y1': 100, 'x2': 350, 'y2': 100, 'name': 'obs_w', 'orientation': 'diagonal'},
#     '6': {'x1': 350, 'y1': 100, 'x2': 350, 'y2': 50, 'name': 'obs_w', 'orientation': 'diagonal'},
# }

LEVEL_5_WALLS = {
    "1": {"x": 150, "y": 120, "width": 100, "height": 30},
    "2": {"x": 300, "y": 80,  "width": 30,  "height": 60},
    "3": {"x": 450, "y": 120, "width": 100, "height": 30},
    "4": {"x": 600, "y": 180, "width": 30,  "height": 100},
    "5": {"x": 500, "y": 400, "width": 100, "height": 30},
    # "6": {"x": 150, "y": 250, "width": 30,  "height": 200},
    "7": {"x": 300, "y": 500, "width": 150, "height": 30}
}
