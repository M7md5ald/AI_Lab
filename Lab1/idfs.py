from search import Search
from puzzle import Puzzle

class IDFS(Search):
    def idfs(self, puzzle: Puzzle, max_depth_limit=100):
        print("Start state:", puzzle.state)
        self.start_timer()

        for depth_limit in range(max_depth_limit):
            self.depth_limit = depth_limit
            stack = [(puzzle.state, 0)]
            self.visited.clear()
            self.parent.clear()
            self.move_dir.clear()
            self.parent[puzzle.state] = None
            self.move_dir[puzzle.state] = None
            self.max_depth = 0

            while stack:
                current, depth = stack.pop()
                self.max_depth = max(self.max_depth, depth)

                current_puzzle = Puzzle(current)
                if current_puzzle.is_goal():
                    print("Puzzle solved!")
                    print("Search depth:", self.max_depth)
                    print("Solution found at depth limit:", depth_limit)
                    self.print_results(current)
                    return

                if current in self.visited:
                    continue

                if depth >= depth_limit:
                    continue

                self.visited.add(current)

                for neighbor, move in current_puzzle.get_children():
                    if neighbor not in self.visited:
                        self.record_parent(neighbor,current,move)
                        stack.append((neighbor, depth + 1))

            self.stop_timer()

        print("No solution found within depth limit:", max_depth_limit)
        self.print_results(current)
