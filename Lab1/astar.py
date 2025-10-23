from search import Search
from puzzle import Puzzle
import heapq
import math

class AStar(Search):
    def __init__(self, heuristic="manhattan"):
        super().__init__()
        self.g_cost = {}
        self.heuristic = heuristic.lower()

    def a_star(self, puzzle: Puzzle):
        print(f"Start state: {puzzle.state}")
        print(f"Using {self.heuristic.title()} heuristic")
        self.start_timer()

        open_list = []
        g = 0
        h = self.choose_heuristic(puzzle.state)
        f = g + h
        heapq.heappush(open_list, (f, g, puzzle.state))

        self.visited.clear()
        self.parent[puzzle.state] = None
        self.move_dir[puzzle.state] = None
        self.max_depth = 0
        self.g_cost[puzzle.state] = 0

        while open_list:
            current_f, current_g, current = heapq.heappop(open_list)

            if current_g > self.g_cost.get(current, float('inf')):
                continue

            current_puzzle = Puzzle(current)

            if current_puzzle.is_goal():
                self.stop_timer()
                print("Puzzle solved!")
                self.print_results(current)
                return

            if current in self.visited:
                continue
            self.visited.add(current)

            self.max_depth = max(self.max_depth, current_g)

            for board, move in current_puzzle.get_children():
                new_g = current_g + 1
                new_h = self.choose_heuristic(board)
                new_f = new_g + new_h

                if board not in self.visited and (board not in self.g_cost or new_g < self.g_cost[board]):
                    heapq.heappush(open_list, (new_f, new_g, board))
                    self.record_parent(board, current, move)
                    self.g_cost[board] = new_g

        self.stop_timer()
        print("No solution found.")
        self.print_results(current)

    def choose_heuristic(self, state):
        """Select which heuristic to use."""
        if self.heuristic == "euclidean":
            return self.euclidean(state)
        else:
            return self.manhattan(state)

    def manhattan(self, state):
        goal = "012345678"
        s = str(state).zfill(9)
        total_distance = 0

        for i in range(9):
            if s[i] == '0':
                continue
            curr_x, curr_y = divmod(i, 3)
            goal_index = goal.index(s[i])
            goal_x, goal_y = divmod(goal_index, 3)
            total_distance += abs(curr_x - goal_x) + abs(curr_y - goal_y)
        return total_distance

    def euclidean(self, state):
        goal = "012345678"
        s = str(state).zfill(9)
        total_distance = 0

        for i in range(9):
            if s[i] == '0':
                continue
            curr_x, curr_y = divmod(i, 3)
            goal_index = goal.index(s[i])
            goal_x, goal_y = divmod(goal_index, 3)
            dx = curr_x - goal_x
            dy = curr_y - goal_y
            total_distance += math.sqrt(dx * dx + dy * dy)
        return total_distance
