# test_agent.py
import numpy as np
from dqn import DQNAgent
import game_envDQN as env  # Assuming your game environment is in a file called game_env.py

def train_agent(agent, num_episodes=1000):
    for episode in range(num_episodes):
        state = env.reset()  # Reset the game environment
        state = np.reshape(state, [1, agent.state_size])  # Reshape for the neural network
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)  # Agent chooses action
            next_state, reward, done = env.step(action)  # Environment responds
            next_state = np.reshape(next_state, [1, agent.state_size])  # Reshape for the neural network
            agent.learn(state, action, reward, next_state, done)  # Agent learns
            state = next_state  # Update state
            total_reward += reward

        print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

def test():
    # Initialize the game environment
    action_size = env.action_size  # Size of the action space
    state_size = env.state_size    # Size of the state space
    agent = DQNAgent(action_size, state_size)  # Initialize the DQN agent

    # Train the agent
    train_agent(agent, num_episodes=1000)

if __name__ == "__main__":
    test()
