import pygame
from Envs.Complicated_Env1 import GameEnv

if __name__ == '__main__':
    env = GameEnv()
    env.reset()
    done = False
    action = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = 1
                elif event.key == pygame.K_RIGHT:
                    action = 0
                elif event.key == pygame.K_UP:
                    action = 2
                elif event.key == pygame.K_DOWN:
                    action = 3
        observation, reward, done, truncated, info = env.step(action)
    pygame.quit()
