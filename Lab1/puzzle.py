class Puzzle:
    GOAL = 12345678  # integer goal (0 represents the blank tile)

    def __init__(self, state):
        """Initialize puzzle with an integer state."""
        self.state = state

    def to_string(self):
        """Return the puzzle state as a 9-character string (padded with leading zero if needed)."""
        return str(self.state).zfill(9)

    def is_goal(self):
        """Check if the puzzle state matches the goal configuration."""
        # Compare as integer directly for efficiency
        return self.state == Puzzle.GOAL

    def get_children(self):
        """
        Generate all valid moves (children) from the current state.
        Returns a list of tuples: (new_state, move_name)
        where move_name is one of "Up", "Down", "Left", "Right".
        """
        s = self.to_string()
        i = s.index('0')  # find blank position
        moves = []
        directions = [(-3, "Up"), (3, "Down"), (-1, "Left"), (1, "Right")]

        for d, name in directions:
            ni = i + d
            if 0 <= ni < 9:
                # prevent wrapping around rows
                if (d == -1 and i % 3 == 0) or (d == 1 and i % 3 == 2):
                    continue

                new_s = list(s)
                new_s[i], new_s[ni] = new_s[ni], new_s[i]  # swap 0 with neighbor
                new_state = int("".join(new_s))
                moves.append((new_state, name))

        return moves
