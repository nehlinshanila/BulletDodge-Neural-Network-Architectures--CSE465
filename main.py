from Envs.Complicated_Env1 import GameEnv
import pygame


def main():
    env = GameEnv()
    env.reset()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = env.action_space.sample()

        observation, reward, done, truncated, info = env.step(action)

    env.close()


if __name__ == '__main__':
    main()
