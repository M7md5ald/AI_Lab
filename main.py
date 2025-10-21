from array import *
import heapq
import time
GOAL = 12345678
def print_moves(goal_val, parent_dict, moves_dict, visited_set):
    path = []
    moves = []
    while goal_val is not None:
        path.append(goal_val)
        moves.append(moves_dict.get(goal_val))
        goal_val = parent_dict.get(goal_val)

    moves = moves[::-1][1:]  # remove None (start)
    print("number of nodes expanded:", len(visited_set))
    print("cost of path is:", len(moves))
    print("path to goal:", " → ".join(moves))

class dfs :
   def __init__(self):
        self.visited = set()
        self.parent = {}
        self.move_dir = {}
        self.max_depth =0

   def dfs(self, start):
    print("start", start)
    stack = [(start, 0)]
    self.visited.clear()
    self.parent[start ] = None
    self.move_dir[start ] = None
    self.max_depth =0
    

    while stack:
        current , depth= stack.pop()
        self.max_depth= max(self.max_depth , depth)
        if current == GOAL:
            print("Puzzle solved!")
            print("Search depth:", self.max_depth)
            print_moves(current, self.parent, self.move_dir, self.visited)
            return

        self.visited.add(current)
        for neighbor, move in self.get_childs(current):
            if neighbor not in self.visited:
                self.parent[neighbor ] = current
                self.move_dir[neighbor ] = move
                stack.append((neighbor , depth+1) )
    print("No solution found")
    print("Search depth:", self.max_depth)


   def get_childs(self, state):
       #convert int state to str to get possible moves
        s = str(state)
       # 013425786 i need to padd with one leading zero cause in this case it isnot the goal
       # if len(s) == 8 :
        #  return []
        
        if len(s) == 8 and s== "12345678":
         return []
        else :
          s = str(s).zfill(9)
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
                moves.append((int("".join(new_s)), name))
        return moves

 
        
class Astar:
    def __init__(self):
        self.visited = set()
        self.moves ={}
        self.parent={}
        self.max_depth=0
        
    def a_star(self , start):
        open_list = []  
        g = 0
        h = self.manhattan(str(start))
        f = g + h
        heapq.heappush(open_list, (f, g, start))  
        self.visited=set()
        self.parent[start] = None
        self.moves[start ] = None
        self.max_depth =0
        while open_list :
            current_f , current_g , current = heapq.heappop(open_list)
            if current == GOAL :
                print("puzzle solved !")
                print("Search depth:", self.max_depth)
                print_moves(current, self.parent, self.moves, self.visited)
                return
                
            self.visited.add(current)
            #max number of moves from start
            self.max_depth = max(self.max_depth , current_g)
            for board , new_h , move in self.get_childs(current):
                if board not in self.visited :
                  new_f = new_h + current_g +1
                  heapq.heappush(open_list, (new_f, current_g+1, board) )
                  self.parent[board] = current
                  self.moves[board]=move
          
        print("No Solution found ")
        print("Search depth:", self.max_depth)
       
    
    def get_childs(self, state):
       #convert int state to str to get possible moves
        s = str(state)
        if len(s) == 8 and s== "12345678":
         return []
        else :
          s = str(s).zfill(9)
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
                new_state_int = int("".join(new_s))  # get integer representation
                h = self.manhattan(str(new_state_int))
                #type casting the list to integer to return it to dfs
                moves.append((int("".join(new_s)), h, name)) 
        return moves
    def manhattan(self , curr_state):
     #curr now is integer 
      goal ="012345678"
      total_distance =0
      if len(curr_state) == 8 and curr_state =="012345678":
          return 0
      else:
        curr_state = str(curr_state).zfill(9)    
        for i in range (len(curr_state)):
          #get manhatan distance of each number 1 -> 8
          #div mod is built in function to help me get coordinated of board as grid from string
          if( curr_state[i] =='0') :
              continue
          curr_x , curr_y = divmod(i , 3) 
          goal_number_index = goal.index(curr_state[i])
          goal_x , goal_y = divmod(goal_number_index , 3 )
          #heuristic distance calc.
          total_distance += abs(curr_x - goal_x) +abs(curr_y - goal_y)
          
      return total_distance
          
          
         
        
        
   #manhattan function to calculate each one is away from goal by how many steps
   #put the calculations in heapq and take min one explore 
        

# Example run
initial =  13425786
  # example start state
 #1 2 0
 #3 4 5 
 #6 7 8 
# Run DFS
dfs_search = dfs()
start_time = time.time()
dfs_search.dfs(initial)
end_time = time.time()
print("DFS execution time:", end_time - start_time, "seconds")
print("\n" + "-"*50 + "\n")

# Run A*
astar_search = Astar()
start_time = time.time()
astar_search.a_star(initial)
end_time = time.time()
print("A* execution time:", end_time - start_time, "seconds")