import random

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha        # Learning rate
        self.gamma = gamma        # Discount factor
        self.epsilon = epsilon    # Exploration rate (ε-greedy)
        self.q_table = {}         # Q-table where state is key
        self.q_table_init()

    def q_table_init(self):
        """Initialize Q-table with zeros for all states."""
        pass
    
    def get_q_value(self, state):
        """Retrieve the Q-value for a given state. Returns 0 if not present in the Q-table."""
        return self.q_table.get(state, 0)
    
    def choose_future_state(self, state, valid_future_states):
        """
        Choose an action using epsilon-greedy. 
        With probability epsilon, pick a random action (exploration),
        otherwise pick the action with the highest Q-value (exploitation).
        """
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: randomly choose an action (transition to a valid state)
            return random.choice(valid_future_states)
        else:
            # Exploitation: choose best next state based on max Q-value
            best_action = max(valid_future_states, key=lambda state: self.get_q_value(state))
            return best_action
    
    def update_q_value(self, state, reward, next_state):
        """
        Update the Q-value for the state after observing the reward for the next state.
        """
        # Get current Q-value for the state
        current_q_value = self.q_table.get(state, 0)

        # Get maximum Q-value for the next state
        next_q_value = self.get_q_value(next_state)

        # Update Q-value using the Q-learning formula
        updated_q_value = current_q_value + self.alpha * (reward + self.gamma * next_q_value - current_q_value)

        # Store the updated value in the Q-table
        self.q_table[state] = updated_q_value
