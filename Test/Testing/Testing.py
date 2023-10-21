import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Envs.Simple_Env import GameEnv

if __name__ == '__main__':
    env = GameEnv()
    done = False
    number_of_prey = 2
    number_of_predator = 3

    env.set_agent_number(prey_number=number_of_prey, predator_number=number_of_predator)
    env.agent_init()
    env.reset()

    while not done:
        prey_action = []
        predator_action = []
        for i in range(0, number_of_prey):
            prey_action.append(env.action_space.sample())

        for i in range(0, number_of_predator):
            predator_action.append(env.action_space.sample())

        action = [prey_action, predator_action]

        obs, reward, done, _, _ = env.step(action)

        env.render()
