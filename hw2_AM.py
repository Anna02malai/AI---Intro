def minimax(position : int, depth : int, maximizingPlayer : bool, alpha : float, beta : float, t_values : list, i : int, visited : list):
    
    if depth == 0 and i < 12:                  #If the depth = 0 (ie:) If the tree has reached the terminal node the value is returned
        return int(t_values[i]), i+1, visited
    
    if maximizingPlayer:                       #If it is a maximizer it executes the below code  
        while(depth>0 and i<12):               #Inorder to stop the function calling recursively below depth 0 ,have set the conditions
            for child in generate_children(position):   #to generate the children of the root node and other maximizers have written a function
                max_eval, index, list1 = minimax(child, depth - 1, False, alpha, beta, t_values,i, visited) #Calls the minmax func recursively
                i = index                                   #Updates the values of alpha and others 
                alpha = max(alpha, max_eval) 
                if alpha >= beta and i %4 != 0:         #checks the condition before pruning
                    visited.append(i)
                    i = i + 1                           #skips the terminal node that was pruned
                    return alpha, i, visited            #returns the values 
            return alpha, i, visited                    
    
    else:                   #if it is a minimizer it executes the below code 
        while(depth>=0 and i<12):
            for child in range(1,3):  #to generate the children under the minimizer
                min_eval, index, list1 = minimax(child, depth - 1, True, alpha, beta, t_values,i, visited) #Calls the minmax function recursively
                i = index   # Updates the values of beta and others
                beta = min(beta, min_eval) 
                if alpha >= beta and i %4 != 0:  #checks the conditions before pruning the node
                    visited.append(i), visited.append(i+1) 
                    i = i + 2         #skips the terminal node that was pruned
                    return beta, i, visited   #returns the values
            return beta, i, visited
        
def generate_children(position):     # Return a range of child positions   
    if position == 0:
        return range(0,3)
    else:
        return range(0,2)
   
def main():
    term_val = input("Enter 12 terminal node values: ")   #Accepts input from the User
    t_values = term_val.split()  #Splits the input based on space and stores it in a list
    i = 0
    visited = []
    val, index, list1 = minimax(0,3,True,float('-inf'), float('inf'), t_values, i, visited) #calls the minmax function with the initialized values
    
    for i in list1:           #Obtains the output as list format, SO trying to print it as expected
        print(i, end = " ")   
    
if __name__ == "__main__":
    main()