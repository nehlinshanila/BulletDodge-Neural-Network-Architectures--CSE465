from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from test2 import DotEnv
import os

env = DotEnv()
env.render = True

# vec_env = DummyVecEnv([lambda: env])

model_path = os.path.join('Training', 'Models', 'Test_Model')
log_path = os.path.join('Training', 'Logs')
model = PPO('MlpPolicy', env=env, verbose=1, tensorboard_log=log_path)

model.learn(total_timesteps=300000)

model.save(model_path)
print('Model Saved')

