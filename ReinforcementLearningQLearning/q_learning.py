import random
import pickle

class QLearning:
    def __init__(self, alpha, gamma, epsilon, min_epsilon, decay_rate, pickle_file = None):
        self.alpha = alpha        # Learning rate
        self.gamma = gamma        # Discount factor
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate
        # self.q_table_file_name = q_table_file_name   # Exploration rate (ε-greedy)
        self.q_table = {} 
        if pickle_file:
            self.load_q_table(pickle_file)
        else:
            self.q_table_init()        # Q-table where state is key
        # self.q_table_init()

    def q_table_init(self):
        """Initialize Q-table with zeros for all states."""
        pass
    
    def load_q_table(self, pickle_file):
        """Load Q-table from a pickle file."""
        try:
            with open(pickle_file, 'rb') as file:
                self.q_table = pickle.load(file)
                print("Q-table loaded successfully from", pickle_file)
        except FileNotFoundError:
            print(f"No pickle file found at {pickle_file}. Starting with an empty Q-table.")
    

    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay_rate) 


    def get_q_value(self, state, next_state):
        """Retrieve the Q-value for a given state. Returns 0 if not present in the Q-table."""
        return self.q_table.get((state,next_state), 0)
    
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
            best_action = max(valid_future_states, key=lambda next_state: self.get_q_value(state,next_state))
            return best_action
    
    def update_q_value(self, state, reward, next_state, valid_actions_next_state):
        """
        Update the Q-value for the state after observing the reward for the next state.
        """
        # Get current Q-value for the state
        current_q_value = self.get_q_value(state, next_state)

        # Get maximum Q-value for the next state
        # next_q_value = self.get_q_value(next_state)
        if not valid_actions_next_state:
            next_q_value = 0
        else:
            next_q_value = max(self.get_q_value(next_state, next_action) for next_action in valid_actions_next_state)


        # Update Q-value using the Q-learning formula
        updated_q_value = current_q_value + self.alpha * (reward + self.gamma * next_q_value - current_q_value)

        # Store the updated value in the Q-table
        self.q_table[(state,next_state)] = updated_q_value
