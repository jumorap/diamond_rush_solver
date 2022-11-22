import copy


class BlockInterface:
    def __init__(self, is_collectable, is_movable, is_walkable, name, gameBoard, location=None):
        # document the block
        """
        Parameters
        ----------
        is_collectable : bool
            Whether the block can be collected by the player for example keys or diamonds.
        is_movable : bool
            Whether the block can be moved by the player or not.
        is_walkable : bool
            Whether the player can walk on the block or not.
        """

        self._is_collectable = is_collectable
        self._is_movable = is_movable
        self._is_walkable = is_walkable
        self._name = name
        self._gameBoard = gameBoard

    def walkOver(self):
        pass

    def unwalkOver(self):
        pass

    def interact(self):
        pass

    def unInteract(self):
        pass

    def isReachable(self):
        return False

    def set_is_collectable(self, is_collectable):
        self._is_collectable = is_collectable

    def get_is_collectable(self):
        return self._is_collectable

    is_collectable = property(get_is_collectable, set_is_collectable)

    def set_is_movable(self, is_movable):
        self._is_movable = is_movable

    def get_is_movable(self):
        return self._is_movable

    is_movable = property(get_is_movable, set_is_movable)

    def set_is_walkable(self, is_walkable):
        self._is_walkable = is_walkable

    def get_is_walkable(self):
        return self._is_walkable

    is_walkable = property(get_is_walkable, set_is_walkable)

    def get_gameBoard(self):
        return self._gameBoard

    def set_gameBoard(self, gameBoard):
        self._gameBoard = gameBoard

    gameBoard = property(get_gameBoard, set_gameBoard)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def __str__(self):
        return self.name[0:1]


class Wall(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "Wall", gameBoard)


class Floor(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, True, "Floor", gameBoard)


class Destination(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "Destination", gameBoard)

    def isReachable(self):
        # if there is no more diamonds to collect, the destination is reachable
        return super().get_gameBoard().remainingDiamonds == 0


class Key(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Key", gameBoard)

    def interact(self):
        super().get_gameBoard().has_key = True
        super().set_is_collectable(False)

    def unInteract(self):
        super().get_gameBoard().has_key = False
        super().set_is_collectable(True)

    def isReachable(self):
        return super().get_is_collectable() and super().get_gameBoard().has_key == False


class Diamond(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Diamond", gameBoard)

    def interact(self):
        super().get_gameBoard().remainingDiamonds -= 1
        super().set_is_collectable(False)
        super().get_gameBoard().updateDestinationState()

    def unInteract(self):
        super().get_gameBoard().remainingDiamonds += 1
        super().set_is_collectable(True)
        super().get_gameBoard().updateDestinationState()

    def isReachable(self):
        return super().get_is_collectable()


class KeyDoor(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, False, "KeyDoor", gameBoard)
        self.is_open = False

    def isReachable(self):
        return super().get_gameBoard().has_key == True and super().get_is_collectable() == True

    def interact(self):
        super().get_gameBoard().has_key = False
        super().set_is_collectable(False)
        super().set_is_walkable(True)

    def unInteract(self):
        super().get_gameBoard().has_key = True
        super().set_is_collectable(True)
        super().set_is_walkable(False)

    def get_is_walkable(self):
        return super().get_gameBoard().has_key

    def set_is_walkable(self, is_walkable):
        super().set_is_walkable(is_walkable)

    is_walkable = property(get_is_walkable, set_is_walkable)


class Spikes(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, True, "Spikes", gameBoard)

    def walkOver(self):
        super().set_is_walkable(False)

    def unwalkOver(self):
        super().set_is_walkable(True)


class Rock(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, True, True, "Rock", gameBoard)

    def move(self, from_block, to_block):
        # if to block is a child from Rock object, walkOver is called
        if isinstance(to_block, Rock):
            to_block.walkOver()

    def walkOver(self):
        pass

    def isReachable(self):
        return True


class Magma(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "Magma", gameBoard)

    def walkOver(self):
        pass


class Hole(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "Hole", gameBoard)

    def walkOver(self):
        pass


class Button(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, True, "Button", gameBoard)

    def walkOver(self):
        pass


class DoorButton(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, True, "DoorButton", gameBoard)

    def walkOver(self):
        pass


class Character(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, True, "Character", gameBoard)

    def walkOver(self):
        pass


class BlockGenerator:
    """
    Class to generate all the objects based on a fixed map
    """

    def __init__(self):
        self.map = {
            'R': Rock,
            'D': Diamond,
            'P': Character,
            'M': Wall,
            'W': Magma,
            'A': Destination,
            'C': Floor,
            'K': KeyDoor,
            'L': Key,
            'S': Spikes,
            'H': Hole,
            'B': Button,
            'U': DoorButton,
        }

    def generate(self, target, gameBoard):
        """
        returns a new Object based on the given char
        for example:
        'R' -> Rock
        'D' -> Diamond
        """
        return self.map[target](gameBoard)


class GameBoard:
    def __init__(self, gameMap):
        self.has_key = False
        self.remainingDiamonds = 0
        self.characterLocation = (0, 0)
        self.destinationLocation = (0, 0)
        self.board = self.generateBoard(gameMap, self)
        self.generateNumberOfCollectables()

    def generateBoard(self, gameMap, gameBoard):
        """
        Generates the board based on the given map
        """
        board = []
        generator = BlockGenerator()
        for row in gameMap:
            board.append([generator.generate(target, gameBoard) for target in row])
        return board

    def generateNumberOfCollectables(self):
        """
        Iterates over the board and counts the number of diamonds and keys
        """
        for row in self.board:
            for block in row:
                if block.name == "Diamond":
                    self.remainingDiamonds += 1
                if block.name == "Character":
                    self.characterLocation = (self.board.index(row), row.index(block))
                if block.name == "Destination":
                    self.destinationLocation = (self.board.index(row), row.index(block))

    def updateDestinationState(self):
        destination_row, destination_col = self.destinationLocation
        destination_block = self.board[destination_row][destination_col]

        if self.remainingDiamonds == 0:
            destination_block.set_is_walkable(True)
        else:
            destination_block.set_is_walkable(False)

    def generateVisitedMatrix(self):
        """
        Generates a matrix of the same size as the board, but filled with False
        """
        return [[False for x in range(len(self.board[0]))] for y in range(len(self.board))]

    def getDirectionOfMovement(self, start_point, end_point):
        """
        Moves the character from the start_point to the end_point and returns the direction of the move
        (L, R, U, D)
        """
        direction = ""
        if start_point[0] == end_point[0]:
            if start_point[1] > end_point[1]:
                direction = "L"
            else:
                direction = "R"
        else:
            if start_point[0] > end_point[0]:
                direction = "U"
            else:
                direction = "D"

        return direction

    def isSolved(self):
        """
        Returns True if the map is solved
        """
        if self.characterLocation != self.destinationLocation:
            return False
        print("is solved")
        return True

    def getInstructionsLenght(self, instructions):
        """
        Returns the lenght of the instructions
        """
        lenght = 0
        for instruction in instructions:
            lenght += len(instruction)
        return lenght

    def getSpecialBlocksRecursive(self, location, visited, reachableBlocks, path):
        """
        Recursive function to get the shortest path to all the reachable blocks
        """
        curr_row, curr_col = location

        # get the current block
        block = self.board[curr_row][curr_col]

        # if the current block is a special block, add it to the reachable blocks
        if block.isReachable():
            if block not in reachableBlocks:
                reachableBlocks[block] = copy.deepcopy(path)
            else:
                if len(path) < len(reachableBlocks[block]):
                    reachableBlocks[block] = copy.deepcopy(path)
            return

        # get the next blocks
        next_blocks = self.getNeighbors(location, visited)

        # for each next block, call the function recursively
        for next_block in next_blocks:
            path.append(next_block)
            visited[curr_row][curr_col] = True
            self.getSpecialBlocksRecursive(next_block, visited, reachableBlocks, path)
            path.pop()
            visited[curr_row][curr_col] = False

    def getNeighbors(self, location, visited):
        """
        returns a list of neighbors of the given location
        """
        neighbors = []
        curr_row, curr_col = location
        for next_row, next_col in [[curr_row + 1, curr_col], [curr_row - 1, curr_col], [curr_row, curr_col + 1],
                                   [curr_row, curr_col - 1]]:
            if not (next_row >= 0 and next_row < len(self.board) and next_col >= 0 and next_col < len(self.board[0])):
                continue
            if visited[next_row][next_col]:
                continue
            neighbors.append((next_row, next_col))

        # get the block of each neighbor and check if it is walkable
        neighbors = [neighbor for neighbor in neighbors if self.board[neighbor[0]][neighbor[1]].is_walkable]

        return neighbors

    def __str__(self) -> str:
        map_str = ""
        for row in self.board:
            for block in row:
                map_str += str(block)
            map_str += "\n"
        return map_str

    def moveBack(self, path):
        """
        Moves the character back to the given block reverting the changes made to the board
        """
        # interact with the las element of the path
        end_point = path[-1]
        block = self.board[end_point[0]][end_point[1]]
        block.unInteract()

        # change the character location
        self.characterLocation = path[0]

        # unwalk over the path between the character and the block
        for i in range(1, len(path) - 1):
            row_point = path[i][0]
            col_point = path[i][1]
            self.board[row_point][col_point].unwalkOver()

    def moveTo(self, path):
        """
        Moves the character to the given block

        parameters:
        block: the block to move to, its compossed by an array of points of the map where the character moves
        for example: [(3, 3), (2, 3), (1, 3), (0, 3)] it means that the character moves from (3, 3) to (0, 3)
        incluiding the block (0, 3) in the path
        """
        # interact wiht the last element of the path
        end_point = path[-1]
        end_block = self.board[end_point[0]][end_point[1]]
        end_block.interact()

        # move the character
        self.characterLocation = end_point

        # move the blocks
        for i in range(1, len(path) - 1):
            row_point = path[i][0]
            col_point = path[i][1]
            self.board[row_point][col_point].walkOver()

        # get the list of moves
        list_movements = []
        for i in range(len(path) - 1):
            start_point = path[i]
            end_point = path[i + 1]
            moves = self.getDirectionOfMovement(start_point, end_point)
            list_movements.append(moves)

        return list_movements

    def getShortestSolutionPath(self):
        """
        Returns the shortest path to the solution
        This path should collect all the diamonds
        """
        instructions = []
        best_instructions = []
        visited = {}
        self.getSinlgeSolutionPathRecursive(instructions, visited)
        # self.getBestSolutionPathRecursive(instructions, best_instructions)
        return instructions

    def getSinlgeSolutionPathRecursive(self, instructions, visited):
        """
        Recursive function to get the shortest path to the solution
        """
        # if the character is alrady at the destination, return an empty list
        if self.isSolved():
            return True

        # get the reachable blocks
        reachableBlocks = self.getSpecialBlocksPath()

        # for each reachable block, move to it and call the function recursively
        for i, block in enumerate(reachableBlocks):
            list_movements = self.moveTo(block)
            instructions.extend(list_movements)
            # call the function recursively
            if self.getSinlgeSolutionPathRecursive(instructions, visited):
                return True
            # move back
            self.moveBack(block)
            # remove the moves from the instructions
            for i in range(len(list_movements)):
                instructions.pop()

        return False

    def getBestSolutionPathRecursive(self, instructions, best_instructions):
        if self.isSolved():
            if len(instructions) < len(best_instructions) or len(best_instructions) == 0:
                best_instructions.clear()
                best_instructions.extend(instructions)
            return

            # get the reachable blocks
        reachableBlocks = self.getSpecialBlocksPath()

        # for each reachable block, move to it and call the function recursively
        for i, block in enumerate(reachableBlocks):
            print("step", i, "dimonds", self.remainingDiamonds, "moving to block: ", block)
            # move to the block
            list_movements = self.moveTo(block)
            instructions.extend(list_movements)
            # call the function recursively
            self.getBestSolutionPathRecursive(instructions, best_instructions)
            # move back
            self.moveBack(block)
            # remove the moves from the instructions
            for i in range(len(list_movements)):
                instructions.pop()

    def getSpecialBlocksPath(self):
        """
        starting from the character location, get all the speacial blocks for example diamonds, keys, etc
        """
        # if the character is alrady at the destination, return an empty list
        if self.characterLocation == self.destinationLocation:
            return []

        # list of reachable blocks each element is dict with keys: block, location where location is a list of charters, each character is a location in the board
        reachableBlocks = {}
        # matrix to keep track of visited blocks
        visited = self.generateVisitedMatrix()
        visited[self.characterLocation[0]][self.characterLocation[1]] = True
        # seacht the shortest path to each reachable location
        self.getSpecialBlocksRecursive(self.characterLocation, visited, reachableBlocks, [self.characterLocation])

        # convert the reachable blocks to a list of blocks
        reachableBlocksList = []
        for key in reachableBlocks:
            reachableBlocksList.append(reachableBlocks[key])

        # sort the list based on the lenght of the path
        reachableBlocksList.sort(key=lambda x: len(x))
        return reachableBlocksList
