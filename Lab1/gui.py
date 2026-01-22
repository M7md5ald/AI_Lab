import tkinter as tk
from tkinter import messagebox
from puzzle import Puzzle
from dfs import DFS
from bfs import BFS
from idfs import IDFS
from astar import AStar


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("680x700")
        self.root.configure(bg="midnight blue")

        self.current_state = 125340678
        self.initial_state = 125340678
        self.solution_moves = []
        self.move_index = 0
        self.animating = False

        self.setup_ui()
        self.update_grid()

    def setup_ui(self):
        tk.Label(self.root, text="8-Puzzle Solver", font=("Arial", 20, "bold"),
                 bg="midnight blue", fg="cyan").pack(pady=10)

        top = tk.Frame(self.root, bg="midnight blue")
        top.pack(padx=20, pady=10)

        # Grid
        left = tk.Frame(top, bg="midnight blue")
        left.pack(side=tk.LEFT, padx=20)

        grid = tk.Frame(left, bg="midnight blue")
        grid.pack()

        self.tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(grid, text="", font=("Arial", 32, "bold"), width=3, height=1,
                                 bd=3, bg="navy", fg="white")
                tile.grid(row=i, column=j, padx=2, pady=2)
                row.append(tile)
            self.tiles.append(row)

        # Input
        input_frame = tk.Frame(left, bg="midnight blue")
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="State:", bg="midnight blue", fg="cyan", font=("Arial", 10, "bold")).pack(
            side=tk.LEFT)
        self.entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.entry.insert(0, str(self.current_state))
        self.entry.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Set", command=self.set_state, bg="dark slate gray", fg="white",
                  font=("Arial", 9, "bold")).pack(side=tk.LEFT)

        # Algorithms
        right = tk.Frame(top, bg="midnight blue")
        right.pack(side=tk.LEFT, padx=20)

        tk.Label(right, text="Algorithms", font=("Arial", 12, "bold"), bg="midnight blue", fg="cyan").pack()

        colors = ["crimson", "navy", "purple", "dark slate gray", "olive"]
        for i, name in enumerate(["DFS", "BFS", "IDFS", "A* (Manhattan)", "A* (Euclidean)"]):
            tk.Button(right, text=name, width=18, bg=colors[i], fg="white", font=("Arial", 9, "bold"),
                      command=lambda n=name: self.run_algo(n)).pack(pady=3)

        self.stop_btn = tk.Button(right, text="⏹ Stop", width=18, command=self.stop, state=tk.DISABLED,
                                  bg="red", fg="white", font=("Arial", 9, "bold"))
        self.stop_btn.pack(pady=10)

        # Terminal
        tk.Label(self.root, text="Outputs", font=("Arial", 12, "bold"), bg="midnight blue", fg="cyan").pack()
        self.terminal = tk.Text(self.root, height=20, width=80, bg="black", fg="white", font=("Arial", 12))
        self.terminal.pack(padx=20, pady=10)
        self.terminal.insert("1.0", "Click an algorithm to solve...")

    def update_grid(self):
        s = str(self.current_state).zfill(9)
        for i in range(3):
            for j in range(3):
                val = s[i * 3 + j]
                self.tiles[i][j].config(text="" if val == "0" else val,
                                        bg="dark slate gray" if val == "0" else "cyan",
                                        fg="midnight blue" if val != "0" else "white")

    def set_state(self):
        try:
            self.stop()
            new_state = int(self.entry.get())
            state_str = str(new_state).zfill(9)

            # must be 9 digits
            if len(state_str) != 9:
                messagebox.showerror("Error", "State must be exactly 9 digits!")
                return

            # must contain digits 0-8 exactly once
            if sorted(state_str) != ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                messagebox.showerror("Error", "State must contain each digit 0-8 exactly once!")
                return

            self.current_state = self.initial_state = new_state
            self.update_grid()
            self.write_terminal("State updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid state! Enter a valid number.")

    def write_terminal(self, text):
        self.terminal.delete("1.0", tk.END)
        self.terminal.insert("1.0", text)

    def run_algo(self, name):
        def worker():
                if self.initial_state == Puzzle.GOAL:
                    self.write_terminal("Already at goal state!")
                    return
                puzzle = Puzzle(self.initial_state)
                self.stop()
                if name == "DFS":
                    solver = DFS()
                    solver.dfs(puzzle)
                elif name == "BFS":
                    solver = BFS()
                    solver.bfs(puzzle)
                elif name == "IDFS":
                    solver = IDFS()
                    solver.idfs(puzzle)
                elif "Manhattan" in name:
                    solver = AStar("manhattan")
                    solver.a_star(puzzle)
                else:
                    solver = AStar("euclidean")
                    solver.a_star(puzzle)

                moves, cost = solver.trace_path(Puzzle.GOAL)

                if cost == 0:
                    self.write_terminal("No Solution found!")
                    return

                output = f"{name}\n{'=' * 50}\n"
                output += f"Number of nodes expanded: {len(solver.visited)}\n"
                output += f"Cost of path: {cost}\n"
                output += f"Search Depth: {solver.max_depth}\n"
                output += f"Running Time: {round(solver.running_time(), 6)}s\n"
                output += f"{'=' * 50}\n"
                output += f"Path to goal:\n{' → '.join(moves) if moves else 'none'}\n"
                output += f"{'=' * 50}\n"

                self.solution_moves = moves
                self.write_terminal(output)

                if cost > 0:
                    self.root.after(500, self.animate)

        worker()

    def animate(self):
        if not self.solution_moves:
            return

        self.animating = True
        self.stop_btn.config(state=tk.NORMAL)
        self.current_state = self.initial_state
        self.move_index = 0
        self.update_grid()
        self.root.after(500, self.next_move)

    def next_move(self):
        if not self.animating or self.move_index >= len(self.solution_moves):
            self.animating = False
            self.stop_btn.config(state=tk.DISABLED)
            return

        move = self.solution_moves[self.move_index]
        puzzle = Puzzle(self.current_state)

        # Use the existing get_children method from Puzzle class
        for new_state, move_name in puzzle.get_children():
            if move_name == move:
                self.current_state = new_state
                break

        self.update_grid()
        self.move_index += 1
        self.root.after(500, self.next_move)

    def stop(self):
        self.animating = False
        self.stop_btn.config(state=tk.DISABLED)