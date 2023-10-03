import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame


class DotEnv(gym.Env):
    def __init__(self, screen_width=400, screen_height=400, render_mode='human'):
        super(DotEnv, self).__init__()

        # screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        # defining the agent policies
        self.direction_line_length = 20
        self.game_speed = 1
        self.test_health = 10

        # for Blue dot
        self.blue_dot_radius = 20
        self.blue_dot_health = 5
        self.blue_dot_attack_dmg = 1
        self.blue_dot_search_radius = 100
        self.blue_dot_turn_rate = None
        self.blue_dot_stamina = 50
        self.blue_dot_stamina_recovery_rate = 15

        # for Red dot
        self.red_dot_radius = self.blue_dot_radius - 10
        self.red_dot_health = 50
        self.red_dot_attack_dmg = 1
        self.red_dot_search_radius = None
        self.red_dot_turn_rate = None

        # action space (left, right, up, down) for both
        self.action_space = spaces.Discrete(4)

        # Define observation space (positions of blue dot and red dot)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0], dtype=np.float32),
                                            high=np.array([self.screen_width / 2, self.screen_height, self.screen_width, self.screen_height], dtype=np.float32),
                                            dtype=np.float32)

        # Initializing the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dots Moving Environment')

        # Initializing the positions of the blue and red dots
        self.blue_dot_pos = np.array([self.screen_width / 4, self.screen_height / 2], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)

        # Define grid line properties
        self.grid_color = (0, 0, 0)
        self.grid_spacing = 20  # Adjust this value to change the grid spacing

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        # defining the reward for the agent
        self.total_reward = 0

        self.obstacles = [
            (200, 100, 20, 150),
            (300, 250, 50, 20)
        ]

    def reset(self, seed=0):
        super().reset(seed=seed)

        # Reset the positions of the blue and red dots
        self.blue_dot_pos = np.array([0, 0], dtype=np.float32)
        self.red_dot_pos = np.array([3 * self.screen_width / 4, self.screen_height / 2], dtype=np.float32)


        self.blue_dot_health = self.test_health
        self.total_reward = 0


        # Return the initial observation (concatenate blue dot position and red dot position)
        observation = np.concatenate([self.blue_dot_pos, self.red_dot_pos])
        # print(observation)

        return [observation, seed]


    def collides_with_obstacle(self, position, obstacle):
        # Check if the dot's position collides with the given obstacle
        x, y, width, height = obstacle
        dot_x, dot_y = position
        return (x <= dot_x <= x + width) and (y <= dot_y <= y + height)


    def resolve_collision(self, position, obstacle):
        # Adjust the dot's position to resolve the collision with the obstacle
        x, y, width, height = obstacle
        dot_x, dot_y = position

        # Calculate the nearest valid position outside the obstacle
        new_x = max(x, min(dot_x, x + width))
        new_y = max(y, min(dot_y, y + height))

        position[0] = new_x
        position[1] = new_y

    def step(self, action):
        reward = 0
        done = False
        # Define the movement speed
        move_speed = 0.9 * self.game_speed
        offset = 3
        # unpacking the action for blue and red dots
        action_blue_dot = action
        # print(self.red_dot_pos.dtype, self.red_dot_pos.dtype)

        if action_blue_dot == 0:  # Move blue dot left
            self.blue_dot_pos[0] -= move_speed
            # reward -= 0.01

        elif action_blue_dot == 1:  # Move blue dot right
            self.blue_dot_pos[0] += move_speed
            # reward -= 0.01

        elif action_blue_dot == 2:  # Move blue dot up
            self.blue_dot_pos[1] -= move_speed
            # reward -= 0.01

        elif action_blue_dot == 3:  # Move blue dot down
            self.blue_dot_pos[1] += move_speed
            # reward -= 0.01
        reward += 0.001
        move_speed = 0.05 * self.game_speed

        # Calculate the direction vector from the red dot to the blue dot
        direction = self.blue_dot_pos - self.red_dot_pos

        # Normalize the direction vector
        direction /= np.linalg.norm(direction)
        # print("Direction: ", direction)
        distance_between_centers = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)



        # Clip red dot position to stay within the entire screen
        self.red_dot_pos = np.clip(self.red_dot_pos, [0, 0], [self.screen_width, self.screen_height])

        # Check if the dots collide with each other
        if distance_between_centers < self.blue_dot_radius + self.red_dot_radius:
            # Separate the dots by moving the red dot away from the blue dot
            self.red_dot_pos -= -50.0 + move_speed * direction
            self.blue_dot_health -= self.red_dot_attack_dmg
            if(self.blue_dot_health <= 0):
                done = True
            reward -= 5
            # print("collision")

        else:
            # Move the red dot towards the blue dot with a fixed speed
            self.red_dot_pos += move_speed * direction

        # Clip blue dot position to stay within the first half of the screen
        self.blue_dot_pos[0] = np.clip(self.blue_dot_pos[0], 0, self.screen_width)
        self.blue_dot_pos[1] = np.clip(self.blue_dot_pos[1], 0, self.screen_height)


        # Define a simple reward function (e.g., distance between the two dots)
        # reward = -np.linalg.norm(self.blue_dot_pos - self.red_dot_pos)
        self.total_reward += reward


        # # check for the dots' collision with the obstacles
        # for obstacle in self.obstacles:
        #     if self.collides_with_obstacle(self.blue_dot_pos, obstacle):
        #         self.resolve_collision(self.blue_dot_pos, obstacle)
        #     if self.collides_with_obstacle(self.red_dot_pos, obstacle):
        #         self.resolve_collision(self.red_dot_pos, obstacle)

        # Check if the dots are close to each other (you can adjust the distance threshold as needed)
        # done = np.linalg.norm(self.blue_dot_pos - self.red_dot_pos) < 10

        # print(self.red_dot_pos.dtype, self.red_dot_pos.dtype)

        observation = np.concatenate([self.blue_dot_pos, self.red_dot_pos])

        return observation, reward, done, False, {}

    def display_total_reward(self):
        text_surface = self.font.render(f"Reward: {self.total_reward: .2f} Blue Health: {self.blue_dot_health}", True, (0, 0, 0))

        text_rect = text_surface.get_rect()

        text_rect.center = (self.screen_width - 200, 10)

        self.screen.blit(text_surface, text_rect)

    def render(self):
        if self.render_mode == 'human':
            # Clear the screen
            self.screen.fill((255, 255, 255))

            # Draw grid lines
            for x in range(0, self.screen_width, self.grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.screen_height), 1)
            for y in range(0, self.screen_height, self.grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y), 1)

            # Draw blue dot
            pygame.draw.circle(self.screen, (0, 0, 255), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])), self.blue_dot_radius)

            # draw the blue dot search radius
            pygame.draw.circle(self.screen, (0, 0, 255), (int(self.blue_dot_pos[0]), int(self.blue_dot_pos[1])),
                               self.blue_dot_search_radius, 1)

            # Draw red dot
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.red_dot_pos[0]), int(self.red_dot_pos[1])), self.red_dot_radius)

            # # calculating the position of facing direction lines
            # blue_dot_direction_end = tuple(map(int, self.blue_dot_pos + self.direction_line_length * action_blue))
            # red_dot_direction_end = tuple(map(int, self.red_dot_pos + self.direction_line_length * action_red))
            #
            # # direction line draw
            # pygame.draw.line(self.screen, (0, 0, 255), tuple(map(int, self.blue_dot_pos)), blue_dot_direction_end, 2)
            # pygame.draw.line(self.screen, (255, 0, 0), tuple(map(int, self.red_dot_pos)), red_dot_direction_end, 2)

            self.display_total_reward()

            # Update the display
            pygame.display.update()

            # # Draw rectangular obstacles
            # for obstacle in self.obstacles:
            #     pygame.draw.rect(self.screen, (128, 128, 128), obstacle)

    def collides_with_obstacle(self, position, obstacle):
        # Check if the dot's position collides with the given obstacle
        x, y, width, height = obstacle
        dot_x, dot_y = position
        return (x <= dot_x <= x + width) and (y <= dot_y <= y + height)

    def resolve_collision(self, position, obstacle):
        # Adjust the dot's position to resolve the collision with the obstacle
        x, y, width, height = obstacle
        dot_x, dot_y = position

        # Calculate the nearest valid position outside the obstacle
        new_x = max(x, min(dot_x, x + width))
        new_y = max(y, min(dot_y, y + height))

        position[0] = new_x
        position[1] = new_y


# Example usage of the gym environment
if __name__ == "__main__":
    env = DotEnv()
    done = False
    observation = env.reset()
    while not done:
        action_blue = env.action_space.sample()

        action = action_blue

        observation, reward, done, _, _ = env.step(action)
        env.render()

        # if env.blue_dot_health == 0:
        #     env.close()


