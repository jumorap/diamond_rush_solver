import browser_image
import categorize
import browser_moves
import Solver.solver as solver


def main():
    print("Starting...")
    browser_image.main()
    print("Rebuilding the map...")
    classes = categorize.get_current_classes()
    print("Solving...")
    board = solver.GameBoard(classes)
    print("Moving...")
    solve_matrix = board.getShortestSolutionPath()
    print(solve_matrix)
    browser_moves.main(solve_matrix)


if __name__ == "__main__":
    main()
