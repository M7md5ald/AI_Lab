from search import Search
from puzzle import Puzzle
from collections import deque

class BFS(Search):
    def bfs(self, puzzle: Puzzle):
        self.start_timer()

        queue = deque([(puzzle.state, 0)])
        self.visited.clear()
        self.parent[puzzle.state] = None
        self.move_dir[puzzle.state] = None
        self.max_depth = 0

        while queue:
            current, depth = queue.popleft()
            self.max_depth = max(self.max_depth, depth)

            current_puzzle = Puzzle(current)
            if current_puzzle.is_goal():
                self.stop_timer()
                return

            if current in self.visited:
                continue
            self.visited.add(current)

            for neighbor, move in current_puzzle.get_children():
                if neighbor not in self.visited and neighbor not in self.parent:
                    self.record_parent(neighbor, current, move)
                    queue.append((neighbor, depth + 1))

        self.stop_timer()
