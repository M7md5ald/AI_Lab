from search import Search
from puzzle import Puzzle
from collections import deque

class DFS(Search):
    def dfs(self, puzzle: Puzzle):
        self.start_timer()

        stack = [(puzzle.state, 0)]
        self.visited.clear()
        self.parent[puzzle.state] = None
        self.move_dir[puzzle.state] = None
        self.max_depth = 0

        while stack:
            current, depth = stack.pop()
            self.max_depth = max(self.max_depth, depth)

            current_puzzle = Puzzle(current)
            if current_puzzle.is_goal():
                self.stop_timer()
                return

            if current in self.visited:
                continue
            self.visited.add(current)

            for neighbor, move in current_puzzle.get_children():
                if neighbor not in self.visited:
                    self.record_parent(neighbor, current, move)
                    stack.append((neighbor, depth + 1))

        self.stop_timer()
