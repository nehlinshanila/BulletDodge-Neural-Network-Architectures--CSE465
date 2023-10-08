
class Agent:
    def __init__(self, agent_index, agent):
        self.agent_index = agent_index
        self.agent = agent

    def agent_action(self, action):
        pass

    # def agent_observation(self):
    #     pass

    def agent_step(self, action):
        if action == 0:
            self.agent.pos[0] -= self.agent.move_speed
        elif action == 1:
            self.agent.pos[0] += self.agent.move_speed
        elif action == 2:
            self.agent.pos[1] -= self.agent.move_speed
        elif action == 3:
            self.agent.pos[1] += self.agent.move_speed

        return self.agent.pos

    def agent_reward(self):
        reward = 0
        if self.agent.agent == 'Predator':
            if self.agent.isHit:
                reward -= 1

            if self.agent.health == 0:
                reward -= 20

        if self.agent.agent == 'Prey':
            if self.agent.isHit:
                reward -= 1

            if self.agent.health == 0:
                reward -= 100

            if

    def agent_done(self):
        pass
