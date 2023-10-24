"""
this code here is solely for the handling of agents' collisions to all the walls
it prevents the agent from moving through the wall and also let him move around freely elsewhere
any kind of changes regarding the collision detection or physics can be done here
"""


def detect_collision(agent, walls):
    offset = 9

    for wall in walls:
        # this part is to handle the left side collision of the wall
        if agent.current_position[0] + agent.radius > wall.left and agent.current_position[0] < wall.right:
            if wall.top - offset < agent.current_position[1] < wall.bottom + offset:
                agent.current_position[0] = wall.left - agent.radius

        # this part is to handle the right side collision of the wall
        if agent.current_position[0] - agent.radius < wall.right and agent.current_position[0] > wall.left:
            if wall.top - offset < agent.current_position[1] < wall.bottom + offset:
                agent.current_position[0] = wall.right + agent.radius

        # this part is to handle the top side collision of the wall
        if agent.current_position[1] + agent.radius > wall.top and agent.current_position[1] < wall.bottom:
            if wall.left - offset < agent.current_position[0] < wall.right + offset:
                agent.current_position[1] = wall.top - agent.radius

        # this part is to handle the bottom side collision of the wall
        if agent.current_position[1] - agent.radius < wall.bottom and agent.current_position[1] > wall.top:
            if wall.left - offset < agent.current_position[0] < wall.right + offset:
                agent.current_position[1] = wall.bottom + agent.radius

