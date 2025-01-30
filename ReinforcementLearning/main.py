import time
import pickle
import csv
from game_env import GameEnv
from q_learning import QLearning

def game_loop():
    # Initialize the game environment and Q-learning agent
    env = GameEnv()
    white_agent = QLearning(alpha=0.1, gamma=0.9, epsilon=0.2)
    black_agent = QLearning(alpha=0.1, gamma=0.9, epsilon=0.2)
    
    total_episodes = 1

    all_boards = []
    all_turns_and_colors = []

    for episode in range(total_episodes):
    # Reset game state to start
        state = env.reset()
        
        episode_states = []
        episode_turns_colors = []

        turn_count = 0

        change_turn = 0

        stalemate = False

        done = False
        # Run until game ends (you might want to add a check to stop when the game is over)
        while turn_count < 1000 and not done:  # Limit to 1000 steps # THIS NEEDS TO BE CHANGED TO WHILE NOT DONEs
            # Get the valid next states (representing all possible state transitions)
            valid_future_states = env.get_valid_future_states(state)
            episode_states.append(list(state[0]))
            if (not state[3]):
                turn_count += 1

            if (state[2] == 'W'):
                agent = white_agent
            else:
                agent = black_agent

            episode_turns_colors.append([state[2],turn_count,state[3]])
            # Choose a next state (in Q-learning, we treat the next state as the "action")
            next_state = agent.choose_future_state(state, valid_future_states)
            
            if (turn_count == 18):
                next_state_list = list(next_state)
                next_state_list[1] = 2
                next_state = tuple(next_state_list)
            # Apply the chosen action (transition to the next state)
            # In this simplified model, `next_state` already reflects the result of an action
            # There’s no need to apply anything further; `next_state` is returned directly.
            
            if env.count_occupied_spaces(state) != env.count_occupied_spaces(next_state):
                change_turn = turn_count
            
            if change_turn + 18 <= turn_count:
                stalemate = True
            else:
                stalemate = False

            # NEED TO ENSURE THAT THE STATES ADD THE NEXT_STATE THAT GETS CHOSEN, AND NEED TO ENSURE THAT IF THE NEXT STATE IS A REMOVAL THEN THE 

            # Calculate reward (can be adjusted based on the result of the transition)
            # Example: positive reward for continuing or completing the move

            white_reward, black_reward, win_condition = env.calc_rewards(state,next_state,stalemate)


            if win_condition:
                done = True

            # REWARD IS MOST IMPORTANT, THIS IS WHERE I INTEGRATE THE REWARD VALUE
            # Update the Q-value for the current state to encourage correct actions
            white_agent.update_q_value(state, white_reward, next_state)
            black_agent.update_q_value(state, black_reward, next_state)


            # Move to the next state
            state = next_state


            # Optionally, print or log the board state and Q-table progress
            # if _ % 100 == 0:  # Print every 100 steps
            #     print(f"Step {_}: {state}, Q-table: {agent.q_table}")

            # Sleep to slow down for readability (optional)
            # time.sleep(0.01)
        all_boards.append(episode_states)
        all_turns_and_colors.append(episode_turns_colors)
        # Once done, save the trained Q-table (optional)
        # with open('trained_q_table.pkl', 'wb') as f:
        #     pickle.dump(agent.q_table, f)
    save_states_to_csv(all_boards, 'game_states.csv')
    save_states_to_csv(all_turns_and_colors,'turns_and_colors.csv')
    save_q_table(white_agent.q_table, "white_q_table.pkl")
    save_q_table(black_agent.q_table, "black_q_table.pkl")
    print('done with run through')


def save_q_table(q_table, filename):
    """Saves the given Q-table to a file."""
    with open(filename, 'wb') as f:
        pickle.dump(q_table, f)


def save_states_to_csv(all_states, filename):
    max_length = max(len(episode) for episode in all_states)

    # Pad shorter episodes with empty values
    padded_states = [episode + [''] * (max_length - len(episode)) for episode in all_states]


    transposed_states = list(zip(*padded_states))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # If needed, you can write a header row to describe the episode columns
        writer.writerow([f"Episode {i+1}" for i in range(len(transposed_states))])

        # Write each row of states (each state in a row is across episodes)
        writer.writerows(transposed_states)


if __name__ == "__main__":
    game_loop()
