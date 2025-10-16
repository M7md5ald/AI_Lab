class bfs:
    def __init__(self ):
            self.total_cost=0
            # dictionary for tracking path 
            self.parent_state = {}
            self.visited= set()
    def bfs(self, current_state):
            self.visited = set()
            self.parent_state = {}
            queue = deque([current_state])
            self.parent_state[current_state.string()] = None
            self.visited.add(current_state.string())

            while queue:
                current = queue.popleft()

                if current.is_goal():
                    print("puzzle solved (BFS)")
                    self.print_path(current)
                    return

                neighbors = self.get_valid_moves(current)
                for neighbor in neighbors:
                    s = neighbor.string()
                    if s not in self.visited:
                        self.visited.add(s)
                        self.parent_state[s] = current.string()
                        queue.append(neighbor)

            print("no solution found (BFS)")