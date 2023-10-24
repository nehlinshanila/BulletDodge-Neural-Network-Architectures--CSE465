from Envs.Complicated_Env1 import GameEnv
import pygame


def main():
    env = GameEnv()
    env.reset()
    done = False
    observation = {}
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        action = env.action_space.sample()

        observation, reward, done, truncated, info = env.step(action)

    print(observation)
    env.close()


if __name__ == '__main__':
    main()
