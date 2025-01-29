import numpy as np

# Game parameters
NUM_POSITIONS = 24  # Number of positions on the board
# MAX_PIECES = 9  # Max pieces per player
# ACTIONS_PER_STATE = 20  # Max possible actions
THREES = [[1,2,3],[1,4,7],[2,10,18],[3,6,8],[4,5,6],[5,13,21],[7,15,23],[8,16,24],[9,10,11],[9,12,15],[11,14,16],[12,13,14],[17,18,19],[17,20,23],[19,22,24],[20,21,22]]
ADJACENT_SPACES = [[2,7],[1,3,10],[2,8],[5,7],[4,6,13],[5,8],[1,4,15],[3,6,16],[10,15],[2,9,11,18],[10,16],[13,15],[5,12,14,21],[13,16],[7,9,12,23],[8,11,14,24],[18,23],[10,17,19],[18,24],[21,23],[13,20,22],[21,24],[15,17,20],[16,19,22]]

for i in range(len(THREES)):
    for j in range(3):
        THREES[i][j] = THREES[i][j]-1

for i in range(len(ADJACENT_SPACES)):
    for j in range(len(ADJACENT_SPACES[i])):
        ADJACENT_SPACES[i][j] = ADJACENT_SPACES[i][j]-1


#NEED TO FIX STATE DEFINITION, ADD COLOR OF TURN INSTEAD OF COUNTER, AND ADD PHASE OF GAME (1 OR 2)

class GameEnv:
    def __init__(self, num_positions=NUM_POSITIONS):
        self.num_positions = num_positions
        self.reset()

    def reset(self):
        # Starting game state: empty board, turn = 0 (even for 'X', odd for 'O'), no special conditions
        self.board = [None] * self.num_positions  # None means unoccupied  # Condition to unlock special actions
        self.phase = 1
        self.color = 'B'
        self.condition_met = False
        return (tuple(self.board),self.phase,self.color,self.condition_met)

    def calc_three_in_a_row(self,board,color):

        desiredPositions = self.board_to_indices(board,color)

        count = 0
        threes_indices = []
        for three in THREES:
            j = 0
            for i in range(3):
                val = three[i]
                inArray = False
                while (j < desiredPositions.length):
                    arrVal = desiredPositions[j]
                    if (arrVal == val):
                        inArray = True
                        break
                    elif arrVal > val:
                        break
                    else:
                        j += 1
                
                    if not inArray:
                        break
                if (inArray):
                    count += 1
                    for x in three:
                        threes_indices.append(x)

        return [count,threes_indices]

    def board_to_indices(board,desired):
        positions = []
        for i in range(len(board)):
            if board[i] == desired:
                positions.append(i)
        return positions
    
    def available_indices_for_removal(self,board,color):
        positions = self.board_to_indices(board,color)
        count, threes_indices = self.calc_three_in_a_row(board,color)
        valid_positions = []
        for x in positions:
            if x not in threes_indices:
                valid_positions.append(x)
        if len(valid_positions) < 1:
            return positions
        else:
            return valid_positions

    def toggle_color(color):
        if (color == 'W'):
            return 'B'
        else:
            return 'W'

    def get_valid_future_states(self, state):
        board, phase, color, condition_met = state
        possible_future_states = []

        # Regular moves (empty spots on the board)
        if condition_met:
            condition_met = False
            # color = self.turn_to_color(turn)
            opp_color = self.toggle_color(color)
            positions = self.available_indices_for_removal(board,opp_color)
            
            for position in range(self.num_positions):
                if position in positions:
                    next_board = list(board)
                    next_board[position] = None
                    next_color = self.toggle_color(color)
                    next_state = (tuple(next_board), phase, next_color, condition_met)
                    possible_future_states.append(next_state)

        elif (phase == 1):
            for position in range(self.num_positions):
                if board[position] is None:
                    next_board = list(board)
                    next_board[position] = color
                    next_color = color
                    [curr_threes, x] = self.calc_three_in_a_row(board,color)
                    [future_threes,y] = self.calc_three_in_a_row(next_board,color)
                    if (future_threes > curr_threes):
                        condition_met = True
                    else:
                        next_color = self.toggle_color(color)
                    
                    next_state = (tuple(next_board), phase, next_color, condition_met)

                    possible_future_states.append(next_state)
        else:
            for position in range(self.num_positions):
                if board[position] == color:
                    next_board = list(board)
                    next_board[position] = None
                    num_colored_pieces = len(self.board_to_indices(board,color))
                    if num_colored_pieces < 4:
                        for new_position in range(self.num_positions):
                            if board[new_position] is None:
                                next_board[new_position] = color
                                next_color = color
                                [curr_threes, x] = self.calc_three_in_a_row(board,color)
                                [future_threes,y] = self.calc_three_in_a_row(next_board,color)
                                if (future_threes > curr_threes):
                                    condition_met = True
                                else:
                                    next_color = self.toggle_color(color)
                                
                                next_state = (tuple(next_board), phase, next_color, condition_met)

                                possible_future_states.append(next_state)
                    else:
                        for new_position in ADJACENT_SPACES[position]:
                            if board[new_position] is None:
                                next_board[new_position] = color
                                next_color = color
                                [curr_threes, x] = self.calc_three_in_a_row(board,color)
                                [future_threes,y] = self.calc_three_in_a_row(next_board,color)
                                if (future_threes > curr_threes):
                                    condition_met = True
                                else:
                                    next_color = self.toggle_color(color)
                                
                                next_state = (tuple(next_board), phase, next_color, condition_met)

                                possible_future_states.append(next_state)


        return possible_future_states

    def calc_rewards(self,state,next_state):
        board = state[0]
        next_board = next_state[0]
        reward = 1
        white_reward = 1
        black_reward = 1
        win_condition = False
        return white_reward, black_reward, win_condition
    
    def check_win_condition(self,state):
        board, phase, color, win_condition = state
        if win_condition:
            return False # returns false if in removal phase, since this means that the game is not over
        else:
            white_positions = self.board_to_indices[board,'W']
            black_positions = self.board_to_indices[board,'B']


    # def apply_action(self, state, action):
    #     """
    #     Apply action to state and return the new state.
    #     """
    #     board, turn, unlocked_actions, condition_met = state

    #     # If action is a regular move (e.g., position on board)
    #     if action[1] == 'move':
    #         position = action[0]
    #         if board[position] is None:
    #             next_board = list(board)
    #             # Place a piece ('X' if even turn, 'O' if odd turn)
    #             next_board[position] = 'W' if turn % 2 == 0 else 'B'

    #             # Transition to the next state
    #             next_turn = turn + 1
    #             next_state = (tuple(next_board), next_turn, unlocked_actions, condition_met)
    #             return next_state
        
    #     # Handle special conditions or actions
    #     if action[1] == 'special' and action[0] in unlocked_actions:
    #         # Update to next state as per your game’s mechanics
    #         next_state = (tuple(board), turn + 1, [], True)  # Empty special action set after used
    #         return next_state

    #     raise ValueError(f"Invalid action: {action}")

# print(THREES[8])    
# print(ADJACENT_SPACES[0])
