from Lab1.idfs import IDFS
from puzzle import Puzzle
from dfs import DFS
from bfs import BFS
from astar import AStar

def main():
    initial = 125340678
    puzzle = Puzzle(initial)

    print("\n--- Depth-First Search ---")
    dfs_solver = DFS()
    dfs_solver.dfs(puzzle)

    print("\n--- Breadth-First Search ---")
    bfs_solver = BFS()
    bfs_solver.bfs(puzzle)

    print("\n--- Iterative Search ---")
    idfs_solver = IDFS()
    idfs_solver.idfs(puzzle)

    print("\n--- A* (Manhattan) ---")
    astar_manhattan = AStar("manhattan")
    astar_manhattan.a_star(puzzle)

    print("\n--- A* (Euclidean) ---")
    astar_euclidean = AStar("euclidean")
    astar_euclidean.a_star(puzzle)

if __name__ == "__main__":
    main()
