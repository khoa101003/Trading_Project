from asyncore import read
import gym
import openpyxl as op
import numpy as np
import random

def make_observation(self):
    self.wb = op.load_workbook('C:\AnhKhoa\PyVSC\gym-basic\gym_basic\envs\AAVEUSDT-15m-data.xlsx')
    self.ws = self.wb['AAVEUSDT-15m-data']
    tmp_list = []
    for row in self.ws.iter_rows(min_row=self.start-14, max_row=self.start+self.trading_time*4+5, min_col=2, max_col=10):
        for cell in row:
            #print(cell.value)
            tmp_list.append(cell.value)
    res = np.array(tmp_list).reshape(-1, 9)
    #print(res)
    return res
class TradingEnv(gym.Env):
    
    def __init__(self):
        self.action_space = gym.spaces.Discrete(1)
        self.observation_space = gym.spaces.Discrete(1)
        self.trading_time = 6
        self.start = random.randint(16, 50000)
        self.current = self.start
        self.observation = make_observation(self)
        self.money = 1000
        self.goal = 1100
        self.fail = 900
        self.crypto = 0
        """self.action_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(1,))
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(9,))"""
    def step(self, action):
        self.current+=1

        id=self.current-self.start+14
        curr_price = self.observation[id, 0]
        print(curr_price)
        self.money = self.money - action*curr_price
        self.crypto += action

        if (self.crypto*curr_price + self.money >= self.goal):
            reward = 1
            self.goal = self.crypto*curr_price + self.money * 110 / 100
            self.fail = self.crypto*curr_price + self.money * 90 / 100
        elif (self.crypto*curr_price + self.money <= self.fail):
            reward = -1
            self.goal = self.crypto*curr_price + self.money * 110 / 100
            self.fail = self.crypto*curr_price + self.money * 90 / 100
        else:
            reward = 0
            
        done = False
        if (self.current-self.start >= self.trading_time*4): 
            done = True
        info = {}
        state = [self.money, self.crypto, self.observation[id-14:id+1,:]]
        return state, reward, done, info
    def reset(self):
        self.start = random.randint(16, 50000)
        self.current = self.start
        self.observation = make_observation(self)
        self.money = 1000
        self.goal = 1100
        self.fail = 900
        self.crypto = 0
        return [self.money, self.crypto, self.observation[0:15,:]]

"""env = TradingEnv()
state = env.reset()
print(state[0:2])
done = False
action = 0
reward = 0
while not done:
    action = random.randint(-10, 10)
    state, reward, done, info = env.step(action)
    print(state[0:2])
    print(state[2][-1,0], reward)    """