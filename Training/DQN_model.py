import os
import sys

from Envs.Complicated_Env1 import GameEnv
from stable_baselines3 import DQN

sys.path.insert(1, os.path.join(sys.path[0], '..'))

log_path = os.path.join('Logs', 'Level_01_DQN')
baseline_path = os.path.join('Models', 'Level_01_DQN')

env = GameEnv()
env.reset()
model = DQN('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

model = model.learn(total_timesteps=1000000)

model.save(baseline_path)
