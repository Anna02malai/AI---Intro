#import libraries
import numpy as np

#defining the shape of the environment (i.e., its states)
environment_rows = 4
environment_columns = 4

#defining actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
epsilon = 0.5 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.1 #discount factor for future rewards
learning_rate = 0.3 #the rate at which the AI agent should learn

def parse_input(index):
    i,j = 0, 0
    i = int(index/4)
    if index %4 == 0: 
        i=i-1
    if i == 3:
        i=0
    elif i == 2:
        i=1
    elif i == 1:
        i=2
    elif i == 0:
        i=3

    if index%4 != 0:
        j = index%4 - 1
    else:
        j = 3
    
    return i,j

def create_board(goals, forbidden, wall):
    #Created a 2D numpy array to hold the rewards for each state. 
    #The array contains 4 rows and 4 columns (to match the shape of the environment), and each value is initialized to -0.1.
    rewards = np.full((environment_rows, environment_columns), -0.1)
    for goal in goals: #the goal states are initalized to +100 reward
        i, j = parse_input(int(goal))
        rewards[i, j] = 100.

    f_i, f_j = parse_input(int(forbidden))
    rewards[f_i, f_j] = -100. #the forbidden state is initalized to +100 reward

    w_i, w_j = parse_input(int(wall)) 

    return rewards, w_i, w_j

def is_terminal_state(current_row_index, current_column_index, rewards):
  #checking the state is terminal or not if reward is not equal to -0.1 it is terminal state
  if rewards[current_row_index, current_column_index] != -0.1:
    return True
  else:
    return False

def get_next_action(current_row_index, current_column_index, epsilon, q_values):
  #if a randomly chosen value between 0 and 1 is less than epsilon, 
  if np.random.random() < epsilon:  #then choose the most promising value from the Q-table for this state.
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(4)

#defining a function that will get the next location based on the chosen action
def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

#defining a function to get the optimal policy of each state
def get_optimal_policies(q_values):
    tiles = {}
    for each_tile in range(1, 17):
        row, col = parse_input(each_tile)
        optimal_move = np.argmax(q_values[row, col])
        tiles[each_tile] = optimal_move
    return tiles

#defining the Q-learning algorithm
def learn(rewards, w_i, w_j, q_values):

    for episode in range(100000):#running through 1000000 training episodes

        row_index, column_index = 3, 1 #getting the starting location for this episode

        #exploring by taking actions (i.e., moving) until we reach a terminal state
        while not is_terminal_state(row_index, column_index, rewards): 
            #choosing which action to take (i.e., where to move next)
            action_index = get_next_action(row_index, column_index, epsilon, q_values)
            
            #performing the chosen action, and transitioning to the next state (i.e., move to the next location)
            old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
            row_index, column_index = get_next_location(row_index, column_index, action_index)
            
            #if the agent bumps into a wall then it remains in the same state and gets a reward
            if row_index==w_i and column_index==w_j:
                row_index = old_row_index
                column_index = old_column_index
                reward = rewards[w_i,w_j] #it gains a reward of -0.1 
            
            else: 
            #receive the reward for moving to the new state
                reward = rewards[row_index, column_index]

            #calculating the temporal difference
            old_q_value = q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

            #updating the Q-value for the previous state and action pair
            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index, action_index] = new_q_value

#definging a function to print the output based on the required format
def process_output(output_type, goals, forbidden, wall, state_index, q_values):

    if output_type == "p":
        x = get_optimal_policies(q_values) 

        for each_tile_ind in x:

            if str(each_tile_ind) in goals:
                print(f'{each_tile_ind}\t' + 'goal')
                # output += f'{each_tile_ind}\t' + 'goal' + '\n'
            elif each_tile_ind == int(forbidden):
                print(f'{each_tile_ind}\t' + 'forbid')
            elif each_tile_ind == int(wall):
                print(f'{each_tile_ind}\t' + 'wall-square')
            else:    
                action = x[each_tile_ind]
                string_action = actions[action]
                print(f'{each_tile_ind}\t{string_action.lower()}')
    
    elif output_type == "q":
        s_i, s_j = parse_input(int(state_index))
        x = q_values[s_i, s_j]
        for dir,val in zip(actions,x):
            print(f'{dir.lower()}\t{round(val,2)}')

def main():
    
    q_values = np.zeros((environment_rows, environment_columns, 4))
    np.random.seed(1)
    
    inp = input("Enter input: ").split()
    goals = inp[0:2]
    forbidden = inp[2]
    wall = inp[3]
    output_type = inp[4]
    state_index = -1
    if output_type == "q":
        state_index = inp[5]
    
    rewards, wall_i, wall_j = create_board(goals, forbidden, wall)
    learn(rewards, wall_i, wall_j, q_values)
    process_output(output_type, goals, forbidden, wall, state_index, q_values)

if __name__ == '__main__':
   main()

#Reference : YouTube : https://youtu.be/iKdlKYG78j4?si=NDLBsWNKOreEtIrF