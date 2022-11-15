from Utils import BlockGenerator

class GameBoard:
    def __init__(self, map):
        """
        Parameters
        ----------
        map : array
            The map of the game.

        """
        self.board = self.generateBoard(map)
        self.remainingDiamonds = 0
        self.remainingKeys = 0
        self.totalDiamonds = 0
        self.totalKeys = 0
        self.characterLocation = (0,0)

    def generateBoard(self, map):
        """
        Generates the board based on the given map
        """
        board = []
        generator = BlockGenerator()
        for row in map:
            board.append([generator.generate(target) for target in row])
        return board

    def generateNumberOfCollectables(self):
        """
        Iterates over the board and counts the number of diamonds and keys
        """
        for row in self.board:
            for block in row:
                if block.name == "Diamond":
                    self.totalDiamonds += 1
                    self.remainingDiamonds += 1
                if block.name == "Key":
                    self.totalKeys += 1
                    self.remainingKeys += 1