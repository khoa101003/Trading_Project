import gym
class BasicEnv2(gym.Env):
    
    def __init__(self):
        self.action_space = gym.spaces.Discrete(1000)
        self.observation_space = gym.spaces.Box()
    def step(self, action):
        state = 1
    
        if action == 2:
            reward = 1
        else:
            reward = -1
            
        done = True
        info = {}
        return state, reward, done, info
    def reset(self):
        state = 0
        return state