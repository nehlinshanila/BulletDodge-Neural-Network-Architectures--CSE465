import numpy as np

CURVE = -0.03
ASCEND = 0.02
CLAMP = 10


class HandleAgentReward:
    def __init__(self):
        self.agent_current_placement = None

    def get_agent_reward(self, agent_pos, walls, goal_coordinate, seen):
        reward = 0

        if seen:
            direction = goal_coordinate - agent_pos
            distance = np.linalg.norm(direction)
            reward += ASCEND * np.exp(CURVE * distance) - CLAMP

        if agent_pos[0] > goal_coordinate[0] and agent_pos[1] < goal_coordinate[1]:
            done = True
            reward = 200

        reward += 0.001

        return reward
