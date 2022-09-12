import browser_image
import categorize


def main():
    print("Starting...")
    browser_image.main()
    print("Rebuilding the map...")
    classes = categorize.get_current_classes()
    print("Finishing...")
    categorize.print_matrix(classes)


if __name__ == "__main__":
    main()
