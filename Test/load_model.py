from stable_baselines3 import PPO

from stable_baselines3.common.evaluation import evaluate_policy
from test2 import DotEnv
import os

env = DotEnv()
model_path = os.path.join('Training', 'Models', 'Test_Model')


model = PPO.load(model_path)

print('Evaluating the model')
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=True)
print(f"Mean Reward: {mean_reward}, Std Reward: {std_reward}")
