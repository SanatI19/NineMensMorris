import time
from game_env import GameEnv
from q_learning import QLearning

def game_loop():
    # Initialize the game environment and Q-learning agent
    env = GameEnv()
    agent = QLearning(alpha=0.1, gamma=0.9, epsilon=0.2)
    
    # Reset game state to start
    state = env.reset()
    
    # Run until game ends (you might want to add a check to stop when the game is over)
    for _ in range(1000):  # Limit to 1000 steps
        # Get the valid next states (representing all possible state transitions)
        valid_future_states = env.get_valid_future_states(state)

        # Choose a next state (in Q-learning, we treat the next state as the "action")
        next_state = agent.choose_future_state(state, valid_future_states)
        
        # Apply the chosen action (transition to the next state)
        # In this simplified model, `next_state` already reflects the result of an action
        # There’s no need to apply anything further; `next_state` is returned directly.
        
        # Calculate reward (can be adjusted based on the result of the transition)
        reward = 1  # Example: positive reward for continuing or completing the move

        # Update the Q-value for the current state to encourage correct actions
        agent.update_q_value(state, reward, next_state)

        # Move to the next state
        state = next_state

        # Optionally, print or log the board state and Q-table progress
        if _ % 100 == 0:  # Print every 100 steps
            print(f"Step {_}: {state}, Q-table: {agent.q_table}")

        # Sleep to slow down for readability (optional)
        time.sleep(0.01)

    # Once done, save the trained Q-table (optional)
    # with open('trained_q_table.pkl', 'wb') as f:
    #     pickle.dump(agent.q_table, f)

if __name__ == "__main__":
    game_loop()
