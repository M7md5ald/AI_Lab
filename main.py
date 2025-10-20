from array import *
import copy
class board:
     goal = 12345678 
     def __init__(self, value):
        self.value = value
        
     def is_goal(self):
        return self.value == self.goal 
     
     def __eq__(self, other):
        return self.value == other.value

     def __hash__(self):
        return hash(self.value)
     
class dfs :
   def __init__(self):
        self.visited = set()
        self.parent = {}
        self.move_dir = {}
        self.max_depth =0

   def dfs(self, start):
    print("start", start.value)
    stack = [(start.value , 0)]
    self.visited.clear()
    self.parent[start.value] = None
    self.move_dir[start.value] = None
    self.max_depth =0
    

    while stack:
        current , depth= stack.pop()
        self.max_depth= max(self.max_depth , depth)
        if current == board.goal:
            print("Puzzle solved!")
            print("Search depth:", self.max_depth)
            self.print_moves(current )
            return

        self.visited.add(current)
        for neighbor, move in self.get_childs(board(current)):
            if neighbor.value not in self.visited:
                self.parent[neighbor.value] = current
                self.move_dir[neighbor.value] = move
                stack.append((neighbor.value , depth+1) )
    print("No solution found")
    print("Search depth:", self.max_depth)


   def get_childs(self, state):
       #convert int state to str to get possible moves
        s = str(state.value)
        #print("here" , s)
        #get index of zero
        i = s.index('0')
        #print(i)
        moves = []
        dirs = [(-3, "Up"), (3, "Down"), (-1, "Left"), (1, "Right")]

        for d, name in dirs:
            #index of zero + possible move up down left right 
            #then check if it is possible
            ni = i + d
            if 0 <= ni < 9:
                # prevent moving left from left corner and right from right corner
                if (d == -1 and i % 3 == 0) or (d == 1 and i % 3 == 2):
                    continue
                #strings in py not like cpp it is immutable so i need to convert it to list to swap
                new_s = list(s)
                new_s[i], new_s[ni] = new_s[ni], new_s[i]
                #type casting the list to integer to return it to dfs
                moves.append((board(int("".join(new_s))), name))
        return moves

   def print_moves(self, goal_val ):
        path = []
        moves = []
        while goal_val is not None:
            path.append(goal_val)
            moves.append(self.move_dir[goal_val])
            goal_val = self.parent[goal_val]
        
        print("number of nodes expanded : " , self.visited.__len__())
        moves = moves[::-1][1:]# remove None (start)
        print("cost of path is : ",moves.__len__())
        print("path to goal : ", " → ".join(moves))
#class Astar:
   # def __init__():
        

# Example run
b1 = board(120345678)
search = dfs()
search.dfs(b1)