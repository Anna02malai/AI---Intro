from heapq import heappush, heappop

def a_star(curr_state):
    parent, g_value, f_value, visited = {}, {}, {}, set()     #used the dictionaries to store the parent,child states, actual cost and estimated cost as keys and values
    visited.add(curr_state)
    g_value[curr_state] = 0
    f_value[curr_state] = heuristic(curr_state)
    queue = [(f_value[curr_state], curr_state)]

    while queue:
        _, state = heappop(queue)    #poping the 1st node in queue once expanded
        if state == "1w2w3w4w":
            return parent            #checks whether the current state has reached the goal state

        for i in range(0, 4):
            new_state, init_state = flip(state, i)  #flipping the pancakes to get the child states
            cost = i + 1
            new_g_value = g_value[state] + cost  #updating the actual cost by adding the cost of flip

            if new_state not in visited or new_g_value < g_value[new_state]:
                visited.add(new_state)                                     #adds the state to visited to avoid visiting same states
                g_value[new_state] = new_g_value                           #assigns the new cost
                f_value[new_state] = new_g_value + heuristic(new_state)    #calculates the estimated cost of the state
                parent[new_state] = (init_state, cost)                     #stores the parent state and cost in the dict

                heappush(queue, (f_value[new_state], new_state))           #pushes the values in the queue to maintain the heap structure and queue

def heuristic(state):
    # Heuristic: Largest ID the pancakes that is out of place
    goal_state = "1234"
    curr_state = ""
    for i in state:       #Converts the state (for eg: "2w1b3w4b") to just a string of integers
        if i.isdigit():
            curr_state += i
   
    h_val = []
    for i,j in zip(goal_state,curr_state):     #compares the outpt state's and current state's pancake order and returns the IDs
        if i==j:
            h_val.append(0)
        else:
            h_val.append(int(j))            
    
    return max(h_val)           #It returns the maximum value of the pancake out of order and returns it as Heuristic cost

def flip(stack, i):     #Flip function that accepts the state and the index of the flip
    state, side = pancakes(stack)   #segrates the order of pancake and burnt and unburnt to seperate lists
    list1 = state[:i+1][::-1] + state[i+1:]
    list2 = side[:i+1][::-1]  + side[i+1:]
    list2 = list(map(lambda x:'b' if x == 'w' else 'w',list2[:i+1])) + list2[i+1:]  #After flipping it maps the element's burnt and unburnt sides accordingly
    new_state = [str(list1[i]) + list2[i] for i in range(len(list1))]
    curr_state = ''.join(new_state)        #returns the flipped state as current state
    out_state = stack[:(i+1)*2] + '|' + stack[(i+1)*2:]
    return curr_state, out_state           #returns the flipped state with the flipped symbol "|" as out_state (for eg: 1w2b|3w4b)

def pancakes(state):     # it seperates the states order and burnt and unburnt sides into 2 seperate lists
    order = [int(state[i]) for i in range(0, len(state), 2)]
    burnt = [state[i + 1] for i in range(0, len(state), 2)]
    return order, burnt

def bfs(curr_state):
    parent, visited = {}, set()   #used parent to store the child and parent states as key and value in Dict and visited as set to avoid duplicates
    visited.add(curr_state)
    queue = [curr_state]

    while len(queue)>0:
        state = queue.pop(0)  #poping the queue once the state is expanded to move to next state in the fringe
        if state == "1w2w3w4w":
            return parent
        
        for i in range(0,4): 
            new_state, init_state = flip(state, i) #flipping the pancake to get the next/child states
            if new_state not in visited:   #if the state is new and not visited it is added in the fringe and queue/visited
                visited.add(new_state)
                parent[new_state] = init_state
                queue.append(new_state)

def main():
    initial_state = input("Enter the Input state: ")    
    [start_state, algo] = initial_state.split("-")
    goal_state = "1w2w3w4w"

    if algo == "b":   
        soln_steps = bfs(start_state)       #Runs the BFS search method and returns a dict full of flipped states till goal state
        tree = []
        while goal_state in soln_steps:     #It fetches the goal state and retraces its parent's state from the whole dict and stores it in the tree list
            parent_state = soln_steps[goal_state]
            tree.append(parent_state)
            goal_state = parent_state.replace('|','')
        
        tree.insert(0, "1w2w3w4w")
        tree.reverse()
        for ele in tree:                    #Prints the output steps from the tree list in the expected format
            print(ele)         

    elif algo == 'a':                       #Runs the BFS search method and returns a dict full of flipped states till goal state
        soln_steps = a_star(start_state)
        path,total_cost = [],[]        
        while goal_state in soln_steps:     #It fetches the goal state and retraces its parent's state and cost from the whole dict and stores it in the path, cost list
            parent_state, cost = soln_steps[goal_state]
            path.append(parent_state)
            total_cost.append(cost)
            goal_state = parent_state.replace('|','')

        path.insert(0, "1w2w3w4w")
        path.reverse(), total_cost.reverse()  #The list is reversed and goal_state and initial cost are added to list
        total_cost.insert(0,0)
        state_cost = 0
        for i,j in zip(path,total_cost):      #The loop runs and prints the steps(output states) in the expected format
            state_cost += j
            h_val = heuristic(i.replace('|',''))
            print(f"{i} g: {state_cost}, h: {h_val}")
    
    else:
        print("Invalid Input")

if __name__ == "__main__":
    main()