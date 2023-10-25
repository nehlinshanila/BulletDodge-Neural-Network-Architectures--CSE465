import math
from RayCasting_Walls import calculate_wall_intersection, OBSTACLES
# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FOV_RADIUS = 100
PREDATOR_RADIUS = 15
AGENT_COLOR = (255, 0, 0)
FOV_COLOR = (0, 0, 255)


def get_fov_rays(agent_position):
    fov_rays = []
    x, y = agent_position

    for angle in range(0, 360, 5):  # Cast rays every 5 degrees
        radians = math.radians(angle)
        dx = math.cos(radians)
        dy = math.sin(radians)
        obs_id = 0  # Default id if ray doesn't intersect with any screen
        remaining_distance = FOV_RADIUS

        for r in range(1, FOV_RADIUS + 1):
            ray_x = int(x + r * dx)
            ray_y = int(y + r * dy)

            for obs_name, data in OBSTACLES.items():
                if data['check'](ray_x, ray_y):
                    obs_id = data.get('id', 0)  # Add a default 'id' value if it's present in the 'data' dictionary
                    remaining_distance = min(remaining_distance, r)
                    break
        fov_rays.append([angle, remaining_distance, str(obs_id)])

    return fov_rays


# enumerate technique for 2 toop into 1
# def render(agent_position, fov_rays):
#     screen.fill((255, 255, 255))  # Clear the screen

#     # Draw the agent as a circle
#     agent_x, agent_y = agent_position
#     pygame.draw.circle(screen, AGENT_COLOR, (agent_x, agent_y), PREDATOR_RADIUS)

#     # Draw the FOV border
#     for angle, distance, _ in fov_rays:
#         radians = math.radians(angle)
#         end_x = int(agent_x + distance * math.cos(radians))
#         end_y = int(agent_y + distance * math.sin(radians))
#         pygame.draw.line(screen, FOV_COLOR, (agent_x, agent_y), (end_x, end_y), 2)

#     pygame.draw.rect(screen, (0, 255, 0), (300, 300, 100, 100))  # Example dimensions and color

#     pygame.display.flip()

# if __name__ == '__main__':
#     agent_position = (10, 300)  # Change this to the agent's position

    # start_time = time.time()
    # fov_rays = get_fov_rays(agent_position)
    # end_time = time.time()

    # # id string. need to encode 

    # # Print the list
    # print(fov_rays)
    # for angle, distance, obs_id in fov_rays:
    #     print(f"Angle: {angle}, Distance: {distance}, Obs ID: {obs_id}")

    # # Calculate and print the elapsed time
    # elapsed_time = end_time - start_time
    # print(f"Time taken to calculate FOV: {elapsed_time:.5f} seconds")

    # # Count the number of rays in the FOV
    # num_rays = len(fov_rays)
    # print(f"Number of rays in the FOV: {num_rays}")

    # # Print the number of FOV rays
    # print(f"Number of FOV rays: {len(fov_rays)}")
    # print(fov_rays)



    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #     render(agent_position, fov_rays)

    # pygame.quit()