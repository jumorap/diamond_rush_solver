import browser_image
import categorize
import browser_moves
import Solver.solver as solver


def main():
    print("Starting...")
    browser_image.start_browser()
    while True:
        try:
            input("Enter here to take a screenshot of the map: ")
            browser_image.start_game()
            print("Saved!")
            print("Rebuilding the map...")
            classes = categorize.get_current_classes()
            print(categorize.print_matrix(classes))
            print("Solving...")
            board = solver.GameBoard(classes)
            print("Moving...")
            try:
                solve_matrix = board.getShortestSolutionPath()
                print(solve_matrix)
                browser_moves.main(solve_matrix)
            except:
                print("No solution found")
        except NameError as e:
            print(e)


if __name__ == "__main__":
    main()
