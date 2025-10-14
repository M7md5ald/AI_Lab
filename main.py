from array import *
import copy
class board:
     goal =  [[ 0, 1 , 2 ] , [ 3 , 4 , 5 ] , [6 , 7 , 8]]
     def __init__(self , array) :
         self.array = array
     def is_goal(self ):
         return self.array == self.goal  
     #def print_board(self):
      #
      # code
      #       
     def blank_tile(self) :
         for i in range(3):
             for j in range(3) :
                 if self.array[i][j] == 0 :
                     return i, j  
     def __eq__(self, other):
       return self.array == other.array
     
class dfs :
    def __init__(self ):
        self.total_cost=0
        # dictionary for tracking path 
        self.parent_state = {}
        self.visited= []
        
    def dfs (self , current_state):
        self.visited =[]
        self.parent_state={}
        stack = [current_state]
        self.parent_state[current_state ]=None
        while stack:
            current= stack.pop()
            if(current.is_goal()):
                print("puzzle solved ")
                break
            self.visited.append(current)
            for neighbor in self.get_valid_moves(current) :
                if neighbor not in self.visited :
                    self.visited.append(neighbor)
                    self.parent_state[neighbor]= current
                    stack.append(neighbor)
        print("no solution found ")
            
    
    def get_valid_moves (self , current_state ):
        #current indexs of 0 in board
        row , col = current_state.blank_tile()
        neighbors= [] #aka childreen states
        dx=[0 , 0 , -1 , 1]
        dy=[1 , -1 , 0 , 0]
        for i in range(4) :
            new_row = dx[i]+row
            new_col = dy[i]+col
            if (new_row < 3 and new_col< 3) and (new_row>= 0 and new_col >= 0): # is it valid move?
               child= copy.deepcopy(current_state)
               child.array[row][col], child.array[new_row][new_col] = child.array[new_row][new_col], child.array[row][col]
               neighbors.append(child) 
        return neighbors   

b1 = board([[1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]])

print(b1.is_goal() )

search = dfs()
search.dfs(b1)