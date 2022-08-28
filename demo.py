import gym 
import random

env = gym.make("gym_basic:trading_env")

state = env.reset()
print(state[0:2])
done = False
action = 0
reward = 0
while not done:
    action = random.randint(-10, 10)
    state, reward, done, info = env.step(action)
    print(state[0:2])
    print(state[2][-1,0], reward)

"""from stable_baselines.common.env_checker import check_env
check_env(env)"""