import time

class Search:
    def __init__(self):
        self.visited = set()
        self.parent = {}
        self.move_dir = {}
        self.max_depth = 0
        self.start_time = 0
        self.end_time = 0

    def start_timer(self):
        """Start measuring execution time."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop measuring execution time."""
        self.end_time = time.time()

    def running_time(self):
        """Return total running time in seconds."""
        return self.end_time - self.start_time

    def record_parent(self, child, parent, move):
        """Store how this state was reached."""
        self.parent[child] = parent
        self.move_dir[child] = move

    def trace_path(self, goal_state):
        """
        Reconstruct the path of moves from start to goal.
        Returns (moves_list, cost).
        """
        path = []
        moves = []
        state = goal_state

        while state is not None:
            path.append(state)
            moves.append(self.move_dir.get(state))
            state = self.parent.get(state)

        moves = moves[::-1][1:]  # remove the initial None
        return moves, len(moves)
