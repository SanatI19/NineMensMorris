import numpy as np
from game_env import GameEnv

# Load Q-table
q_table = np.load("q_table.npy")

env = GameEnv()
state = env.reset()
done = False

while not done:
    action = np.argmax(q_table[state[1]])  
    state, _, done = env.step(action)
    print(f"Action: {action}, New State: {state}")
