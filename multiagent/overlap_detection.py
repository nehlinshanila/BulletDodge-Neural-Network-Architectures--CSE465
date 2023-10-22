
# data structure like a 2D range tree, which can help speed up range searching using library
from sortedcontainers import SortedDict
from fov_points import get_fov_points
from constants import WALLS, SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS

#! time complexity is O(n log n)
# Creating the SortedDict: O(n log n)
# Iterating through the FOV points: O(n)
# Finding overlapping x-ranges: O(log n)
# Determining which walls are overlapping: O(1)
# Since the function iterates through the FOV points, the overall time complexity is O(n log n).
def detect_overlapping_points(agent_position, walls):
    fov_points = get_fov_points(agent_position)
    overlapping_walls = {}

    # Create a SortedDict to efficiently query wall x-ranges
    wall_x_ranges = SortedDict()
    # Initialize a dictionary to track wall IDs
    wall_ids = {}

    # Iterate through the walls
    for wall_id, wall_data in walls.items():
        x_wall, y_wall = wall_data['x'], wall_data['y']
        width, height = wall_data['width'], wall_data['height']
        # Store the wall's x-range in the sorted dictionary
        wall_x_ranges[x_wall] = x_wall + width
        # Create a mapping from x-range to wall ID for efficient lookup
        wall_ids[x_wall] = wall_id

    # Iterate through the FOV points
    for fov_point in fov_points:
        x_fov, y_fov = fov_point
        # Use the irange method to find wall x-ranges overlapping with the FOV point
        overlapping_x_ranges = wall_x_ranges.irange(x_fov - FOV_RADIUS, x_fov + FOV_RADIUS)
        # Iterate through the overlapping x-ranges and determine which walls are overlapping
        for x_range in overlapping_x_ranges:
            wall_id = wall_ids[x_range]
            if wall_id in overlapping_walls:
                overlapping_walls[wall_id].append(fov_point)
            else:
                overlapping_walls[wall_id] = [fov_point]

    #? Print the information
    # for wall_id, coordinates in overlapping_walls.items():
    #     print(f"FOV is overlapping with Wall {wall_id}:")
    #     for coord in coordinates:
    #         x_coord, y_coord = coord
    #         print(f"    Coordinates: ({x_coord}, {y_coord})")

    return overlapping_walls

# def detect_overlapping_walls(agent_position, walls):
#     fov_points = get_fov_points(agent_position)
#     overlapping_walls = {}

#     # Create a SortedDict to efficiently query wall x-ranges
#     wall_x_ranges = SortedDict()
#     # Initialize a dictionary to track wall IDs
#     wall_ids = {}

#     # Iterate through the walls
#     for wall_id, wall_data in walls.items():
#         x_wall, y_wall = wall_data['x'], wall_data['y']
#         width, height = wall_data['width'], wall_data['height']
#         # Store the wall's x-range in the sorted dictionary
#         wall_x_ranges[x_wall] = x_wall + width
#         # Create a mapping from x-range to wall ID for efficient lookup
#         wall_ids[x_wall] = wall_id

#     # Iterate through the FOV points
#     for fov_point in fov_points:
#         x_fov, y_fov = fov_point
#         # Use the irange method to find wall x-ranges overlapping with the FOV point
#         overlapping_x_ranges = wall_x_ranges.irange(x_fov - FOV_RADIUS, x_fov + FOV_RADIUS)
#         # Iterate through the overlapping x-ranges and determine which walls are overlapping
#         for x_range in overlapping_x_ranges:
#             wall_id = wall_ids[x_range]
#             if wall_id in overlapping_walls:
#                 overlapping_walls[wall_id].append(fov_point)
#             else:
#                 overlapping_walls[wall_id] = [fov_point]

#     return overlapping_walls


# nlogn style/ n^2logn
# def detect_overlapping_points(agent_position):
#         fov_points = get_fov_points(agent_position)
#         overlapping_walls = {}  # Dictionary to track overlapping walls
#         # iterates over the coordinates within the agent's FOV.
#         for fov_x_coord, fov_y_coord in fov_points.keys():
#             # iterates over the walls in the environment in the WALLS dictionary.
#             for wall_name, wall_data in WALLS.items():
#                 # variables define the x,y coordinates that belong
#                 # to a certain wall based on its position and dimensions.
#                 wall_x_range = range(wall_data['x'], wall_data['x'] + wall_data['width'])
#                 wall_y_range = range(wall_data['y'], wall_data['y'] + wall_data['height'])
#                 # checks whether the current FOV point is inside the range of
#                 # coordinates for the current wall. If it is, it indicates an overlap.
#                 if fov_x_coord in wall_x_range and fov_y_coord in wall_y_range:
#                     wall_id = wall_data['id']
#                     if wall_id in overlapping_walls:
#                         overlapping_walls[wall_id].append((fov_x_coord, fov_y_coord))
#                     else:
#                         overlapping_walls[wall_id] = [(fov_x_coord, fov_y_coord)]
#         # If an overlap is detected, the code adds its id to the overlapping_walls dictionary.
#         return overlapping_walls




#! time complexity of O((n + m) * log m) 
# where n == number of FOV points, m ==number of walls
#* time complexity closer to O(n log n) but not exactly

# def detect_overlapping_points(agent_position):
#     fov_points = get_fov_points(agent_position)
#     # Data structure will be used to store and query wall x-ranges for overlap detection
#     wall_x_ranges = SortedDict()
#     overlapping_walls = {}  # Dictionary to track overlapping walls

#     # Iterate through the items in the WALLS dictionary.
#     for wall_name, wall_data in WALLS.items():
#         # Extract the x (left boundary) and width (right boundary) of each wall from wall_data
#         # then store this range as a key-value pair in the wall_x_ranges SortedDict
#         # Store the wall's x-range in the sorted dictionary
#         wall_x_ranges[wall_data['x']] = wall_data['x'] + wall_data['width']

#     # Iterate through the keys of the fov_points dictionary
#     for fov_x_coord, fov_y_coord in fov_points.keys():
#         # Use the irange method of the wall_x_ranges SortedDict to find wall names
#         # whose x-ranges overlap with the current X coordinate within the agent's FOV
#         # Find walls that overlap with the current X coordinate
#         overlapping_wall_names = wall_x_ranges.irange(fov_x_coord - FOV_RADIUS, fov_x_coord + FOV_RADIUS)

#         # Iterate through the names of the walls that have overlapping x-ranges with the current X coordinate in the FOV
#         for wall_name in overlapping_wall_names:
#             # Update the overlapping_walls dictionary based on the wall names found to overlap with the current FOV coordinate.
#             if wall_name in overlapping_walls:
#                 overlapping_walls[wall_name].append((fov_x_coord, fov_y_coord))
#             else:
#                 overlapping_walls[wall_name] = [(fov_x_coord, fov_y_coord)]

#     return overlapping_walls

# agent_position = [328.8917, 301.3598]
# overlapping_walls = detect_overlapping_points(agent_position)

# for wall_id, coordinates in overlapping_walls.items():
#     if wall_id in WALLS:  # Check if the wall_id exists in your WALLS dictionary
#         wall_data = WALLS[wall_id]
#         print(f"Wall ID: {wall_id}")
#         for coord in coordinates:
#             print(f"  Intersection coordinates: {coord}")
#     else:
#         print(f"Wall ID {wall_id} not found in WALLS dictionary.")




# agent_position = [328.8917, 301.3598]
# overlapping_walls = detect_overlapping_points(agent_position)

# for wall_name, overlapping_coordinates in overlapping_walls.items():
#     print(f"{wall_name} is overlapping with the agent's FOV at the following coordinates:")
#     for x, y in overlapping_coordinates:
#         print(f"  Coordinate: ({x}, {y})")





# def detect_overlapping_points(agent_position, walls):
#     # Calculate FOV points based on the agent's position (similar to the get_fov_points function)
#     fov_points = get_fov_points(agent_position)

#     overlapping_walls = {}  # Dictionary to store information about overlapping walls with FOV points
#     # Create a SortedDict to efficiently query wall x-ranges
#     wall_x_ranges = SortedDict()
#     # Initialize a dictionary to track wall IDs
#     wall_ids = {}

#     # Iterate through the walls
#     for wall_id, wall_data in walls.items():
#         x_wall, y_wall = wall_data['x'], wall_data['y']
#         width, height = wall_data['width'], wall_data['height']
#         # Store the wall's x-range in the sorted dictionary
#         wall_x_ranges[x_wall] = x_wall + width
#         # Create a mapping from x-range to wall ID for efficient lookup
#         wall_ids[x_wall] = wall_id

#     # Iterate through the FOV points
#     for fov_point in fov_points:
#         x_fov, y_fov = fov_point
#         # Use the irange method to find wall x-ranges overlapping with the FOV point
#         overlapping_x_ranges = wall_x_ranges.irange(x_fov - FOV_RADIUS, x_fov + FOV_RADIUS)
#         # Iterate through the overlapping x-ranges and determine which walls are overlapping
#         for x_range in overlapping_x_ranges:
#             wall_id = wall_ids[x_range]
#             if wall_id in overlapping_walls:
#                 overlapping_walls[wall_id].append((x_fov, y_fov))
#             else:
#                 overlapping_walls[wall_id] = [(x_fov, y_fov)]
                
#     # Print the information
#     for wall_id, coordinates in overlapping_walls.items():
#         for coord in coordinates:
#             x_coord, y_coord = coord
#             print(f"FOV overlapped at wall {wall_id} at coordinates ({x_coord}, {y_coord})")


#     return overlapping_walls

# Example usage:
# Call this function with the agent's position and the wall dictionary.
# overlapping_walls = detect_overlapping_points(agent_position, WALLS)




# def detect_overlapping_points(agent_position):
#     fov_points = get_fov_points(agent_position)
#     overlapping_walls = {}

#     for wall_id, wall_data in WALLS.items():
#         overlapping_points = []  # List to store overlapping FOV points for this wall
#         for fov_x_coord, fov_y_coord in fov_points.keys():
#             if (
#                 wall_data['x'] <= fov_x_coord <= wall_data['x'] + wall_data['width'] and
#                 wall_data['y'] <= fov_y_coord <= wall_data['y'] + wall_data['height']
#             ):
#                 overlapping_points.append((fov_x_coord, fov_y_coord))

#         if overlapping_points:
#             overlapping_walls[wall_id] = {
#                 'wall_data': wall_data,
#                 'overlapping_points': overlapping_points
#             }

#     return overlapping_walls


# agent_position = [328.8917, 301.3598]
# overlapping_walls = detect_overlapping_points(agent_position)
# for wall_id, points in overlapping_walls.items():
#     print(f"Wall {wall_id} has overlapping points: {points}\n")


#* time complexity  O(1) but doesnt work

# def detect_overlapping_walls(agent_position, WALLS):
#     fov_points = get_fov_points(agent_position)  # Get the FOV points using the agent position
#     overlapped_walls = {}  # Initialize the dictionary for overlapping points

#     for fov_point in fov_points:
#         if fov_point in WALLS and WALLS[fov_point] != 0:
#             wall_id = WALLS[fov_point]['id']
#             overlapped_walls[fov_point] = {'coordinates': fov_point, 'id': wall_id}
#  # Add debugging output to check the result
#     print("Overlapping Walls:", overlapped_walls)
#     return overlapped_walls

# if __name__ == '__main':
#     agent_location = [328.8917, 301.3598]

#     overlapping_walls = detect_overlapping_walls(agent_location, WALLS)

#     if overlapping_walls:
#         print(f"Walls overlapping with the agent at {agent_location}:")
#         for point, info in overlapping_walls.items():
#             print(f"Wall ID: {info['id']}, Coordinates: {info['coordinates']}")
#     else:
#         print(f"No walls overlap with the agent at {agent_location}.")





# def detect_overlapping_walls(agent_position, fov_points):
#     overlapping_walls = {}

#     for fov_point in fov_points:
#         # Check if the FOV point overlaps with any walls
#         for wall_name, wall_data in WALLS.items():
#             if is_overlap(wall_data, fov_point):
#                 overlapping_walls[wall_name] = wall_data

#     return overlapping_walls

# def is_overlap(wall_data, fov_point):
#     # Check if the FOV point overlaps with the given wall
#     wall_x, wall_y = wall_data['x'], wall_data['y']
#     wall_width, wall_height = wall_data['width'], wall_data['height']
#     fov_x, fov_y = fov_point

#     return (
#         fov_x >= wall_x and fov_x <= wall_x + wall_width and
#         fov_y >= wall_y and fov_y <= wall_y + wall_height
#     )



# if __name__ == '__main__':
#     agent_position = [328.8917, 301.3598]  # Agent's initial position
#     fov_points = [(330, 280), (320, 220), (390, 260)]  # Sample FOV points

#     overlapping_walls = detect_overlapping_walls(agent_position, fov_points)

#     for wall_id, points in overlapping_walls.items():
#         print(f"Wall {wall_id} has overlapping points: {points}")


# # Example usage
# if __name__ == '__main':
#     agent_position = [328.8917, 301.3598]  # Agent's initial position
#     overlapping_walls = detect_overlapping_walls(agent_position, [])

#     for wall_id, wall_data in overlapping_walls.items():
#         print(f"Agent is overlapping with Wall {wall_id}, has overlapping points: {points}")
        