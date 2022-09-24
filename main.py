import browser_image
import categorize
import browser_moves


def main():
    print("Starting...")
    browser_image.main()
    print("Rebuilding the map...")
    classes = categorize.get_current_classes()
    print("Finishing...")
    categorize.print_matrix(classes)
    print("Moving...")
    browser_moves.main()


if __name__ == "__main__":
    main()
