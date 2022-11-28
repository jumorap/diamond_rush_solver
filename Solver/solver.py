import copy


# utils
def getDirectionOfMovement(start_point, end_point):
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


# given an array delete the element if the next is the same as the current
def deleteDuplicates(array):
    i = 0
    while i < len(array) - 1:
        if array[i] == array[i + 1]:
            del array[i]
            i -= 1
        i += 1
    return array


class BlockInterface:
    def __init__(self, is_collectable, is_movable, is_walkable, name, gameBoard, is_fillable=False):
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
        self._is_fillable = is_fillable
        self._name = name
        self._gameBoard = gameBoard
        self._rock = None  # atribute to save a rock if the block is a rock
        self._location = None  # atribute to save the location of the block
        self.interacted_step = None

    def __repr__(self) -> str:
        return str(self.name) + " at " + str(self.get_position())

    def get_interacted_step(self):
        return self.interacted_step

    def set_interacted_step(self, step):
        self.interacted_step = step

    def has_a_rock(self):
        return self._rock != None  # objects that has a rock cannot be reachable or walkable

    def has_close_rocks(self):
        location = self.get_position()
        closer_rocks = self.get_gameBoard().getCloserRocks(location)
        if len(closer_rocks) > 0:
            return True
        return False

    def get_close_rocks(self):
        location = self.get_position()
        return self.get_gameBoard().getCloserRocks(location)

    def get_rock(self):
        return self._rock

    def can_contain_rock(self):
        return self._is_fillable

    def set_rock(self, rock):
        self._rock = rock

    def get_position(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def walkOver(self):
        pass

    def unwalkOver(self):
        pass

    def interact(self, step=None):
        pass

    def unInteract(self, step=None):
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
        return self._is_walkable and not self.has_a_rock()

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

    def isReachable(self):
        return super().has_close_rocks() == True


class Destination(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, False, "Destination", gameBoard)

    def isReachable(self):
        # if there is no more diamonds to collect, the destination is reachable
        return super().get_gameBoard().remainingDiamonds == 0


class Key(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Key", gameBoard)

    def interact(self, step):
        if super().get_gameBoard().has_key == True:
            return
        if super().get_interacted_step() != None:
            return
        super().set_interacted_step(step)
        super().get_gameBoard().has_key = True
        super().set_is_collectable(False)

    def unInteract(self, step):
        if super().get_gameBoard().has_key == False:
            return
        if super().get_interacted_step() != step:
            return
        super().set_interacted_step(None)
        super().get_gameBoard().has_key = False
        super().set_is_collectable(True)

    def isReachable(self):
        if super().has_a_rock():
            return False
        if super().has_close_rocks():
            return True
        return super().get_is_collectable() and super().get_gameBoard().has_key == False


class Diamond(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Diamond", gameBoard)

    def interact(self, step):
        if self.has_a_rock():
            return
        if super().get_interacted_step() != None:
            return
        super().set_interacted_step(step)
        super().get_gameBoard().remainingDiamonds -= 1
        super().set_is_collectable(False)
        super().get_gameBoard().updateDestinationState()

    def unInteract(self, step):
        if super().get_interacted_step() != step:
            return
        super().set_interacted_step(None)
        super().get_gameBoard().remainingDiamonds += 1
        super().set_is_collectable(True)
        super().get_gameBoard().updateDestinationState()

    def isReachable(self):
        if super().has_a_rock():
            return False
        if super().has_close_rocks():
            return True
        return super().get_is_collectable()


class KeyDoor(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, False, "KeyDoor", gameBoard)
        self.is_open = False

    def isReachable(self):
        return super().get_gameBoard().has_key == True and super().get_is_collectable() == True

    def interact(self, step):
        if super().get_gameBoard().has_key == False:
            return
        if super().get_interacted_step() != None:
            return
        super().set_interacted_step(step)
        super().get_gameBoard().has_key = False
        super().set_is_collectable(False)
        super().set_is_walkable(True)

    def unInteract(self, step):
        if super().get_interacted_step() != step:
            return
        super().set_interacted_step(None)
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

    def isReachable(self):
        if super().has_close_rocks():
            return True


class Rock(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, True, False, "Rock", gameBoard)
        self.visited = super().get_gameBoard().generateVisitedMatrix()

    def move(self, from_block, to_block):
        # if to block is a child from Rock object, walkOver is called
        if isinstance(to_block, Rock):
            to_block.walkOver()

    def visit(self, position):
        row, col = position
        self.visited[row][col] = True

    def unVisit(self, position):
        row, col = position
        self.visited[row][col] = False

    def wasVisited(self, point):
        row, col = point
        return self.visited[row][col]

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
        super().__init__(False, False, False, "Hole", gameBoard, True)

    def get_is_walkable(self):
        return super().has_a_rock()

    def set_is_walkable(self, is_walkable):
        super().set_is_walkable(is_walkable)

    def isReachable(self):
        if super().has_close_rocks() and self.get_is_walkable():
            return True
        return False

    is_walkable = property(get_is_walkable, set_is_walkable)


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

    def __init__(self, gameBoard):
        self.map = {
            'R': self._create_rock,
            'D': Diamond,
            'P': Floor,
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
            'E': Wall
        }
        self.gameBoard = gameBoard

    def _create_rock(self, gameBoard):
        rock = Rock(gameBoard)
        floor = Floor(gameBoard)
        floor.set_rock(rock)
        return floor

    def generate(self, target):
        """
        returns a new Object based on the given char
        for example:
        'R' -> Rock
        'D' -> Diamond
        """
        return self.map[target](self.gameBoard)


class ReachableBlock():
    """
    Class to store the reachable blocks

    Parameters:
    ----------
    block_from: BlockInterface
        the block to where starts the path
    block_to: BlockInterface
        the block to where ends the path
    path: list
        the path to go from block_from to block_to
    """

    def __init__(self, block_from, block_to, path):
        self._block_from = block_from
        self._block_to = block_to
        self._path = path

    def _get_distance(self):
        return len(self._path)

    def _get_block_from(self):
        return self._block_from

    def _get_block_to(self):
        return self._block_to

    def _get_path(self):
        return self._path

    def _get_list_movements(self):
        list_movements = []
        for i in range(len(self.path) - 1):
            start_point = self.path[i]
            end_point = self.path[i + 1]
            moves = getDirectionOfMovement(start_point, end_point)
            list_movements.append(moves)

        return list_movements

    distance = property(_get_distance)
    block_from = property(_get_block_from)
    block_to = property(_get_block_to)
    path = property(_get_path)
    list_movements = property(_get_list_movements)

    def __repr__(self) -> str:
        return f"ReachableBlock({self.block_from}, {self.block_to}, {self.path})"


class GameBoard:
    def __init__(self, gameMap):
        self.has_key = False
        self.remainingDiamonds = 0
        self.characterLocation = (0, 0)
        self.destinationLocation = (0, 0)
        self.board = self.generateBoard(gameMap, self)

    def getBlock(self, point) -> BlockInterface:
        """
        Parameters
        ----------
        point : Tuple(Int)
            The point to return in the map
        """
        return self.board[point[0]][point[1]]

    def getShortestPathsFromRocks(self, rock_location, player_location):
        """
        Parameters
        ----------
        point : Tuple(Int)
            The point to return in the map
        """
        visited = self.generateVisitedMatrix()
        visited[rock_location[0]][rock_location[1]] = True
        player_path = []
        shortest_paths = {}
        self.getShortestPathsFromRocks_recursive(rock_location, player_location, visited, player_path, shortest_paths)
        # iterate over each element of shortest path and if the previus position is the same as the current position, remove it
        for key in shortest_paths:
            path = shortest_paths[key]
            deleteDuplicates(path)
        return shortest_paths

    def getShortestPathsFromRocks_recursive(self, rock_location, player_location, visited, player_path, shortest_paths):
        """
        Parameters
        ----------
        point : Tuple(Int)
            The point to return in the map
        """
        if self.getBlock(rock_location).can_contain_rock():
            if rock_location not in shortest_paths:
                shortest_paths[rock_location] = copy.deepcopy(player_path)
            else:
                if len(player_path) < len(shortest_paths[rock_location]):
                    shortest_paths[rock_location] = copy.deepcopy(player_path)
            return

            # generate the moveable points of the rock
        movable_points = self.getMovablePointRock(rock_location)
        # get the shortest path to each point
        shortest_player_paths = self.getShortestPathFromTo(player_location, movable_points)
        for close_to_rock_point in shortest_player_paths:
            # move the rock to the new point
            new_rock_location_block = self.moverRock(self.getBlock(close_to_rock_point), self.getBlock(rock_location))
            new_rock_location = new_rock_location_block.get_position()
            # if was alredy visited, move back
            if visited[new_rock_location[0]][new_rock_location[1]]:
                self.moveBackRock(self.getBlock(close_to_rock_point), self.getBlock(rock_location))
                continue
            # path that use the player to get to the rock
            path_close_rock_point = shortest_player_paths[close_to_rock_point]
            path_close_rock_point.append(rock_location)
            # mark as visited
            visited[new_rock_location[0]][new_rock_location[1]] = True
            player_path.extend(path_close_rock_point)
            self.getShortestPathsFromRocks_recursive(new_rock_location, rock_location, visited, player_path,
                                                     shortest_paths)
            visited[new_rock_location[0]][new_rock_location[1]] = False
            for _ in range(len(path_close_rock_point)):
                player_path.pop()
            self.moveBackRock(self.getBlock(close_to_rock_point), self.getBlock(rock_location))

    def getCloserRocks(self, position):
        """
        Returns a list with all the blocks near the position that had a rock and can be pushed
        Parameters
        ----------
        position : Tuple(Int)
            The position to check for rocks

        Returns
        -------
        List(BlockInterface)
            A list of all the rocks that are closer to the given position
        """
        row, col = position
        points = [
            ((row + 1, col), (row + 2, col)),
            ((row - 1, col), (row - 2, col)),
            ((row, col + 1), (row, col + 2)),
            ((row, col - 1), (row, col - 2)),
        ]
        closeRocks = []
        for rock_position, opposite_point in points:
            if not self.isInBoard(rock_position):
                continue
            if not self.isInBoard(opposite_point):
                continue
            if not self.getBlock(rock_position).has_a_rock():
                continue
            if self.getBlock(rock_position).get_rock().wasVisited(opposite_point):
                continue
            if self.getBlock(rock_position).can_contain_rock() and self.getBlock(rock_position).has_a_rock():
                continue
            if not self.getBlock(opposite_point).can_contain_rock():
                if not self.getBlock(opposite_point).get_is_walkable():
                    continue
            closeRocks.append(self.getBlock(rock_position))
        return closeRocks

    def getMovablePointRock(self, position):
        """
        Given a rock position, return the point where the rock can be moved
        ----------
        position : Tuple(Int)
            The position to check for rocks

        Returns
        -------
        List(Tuple(Int))
            A list of all the points where the rock can be pushed
        """
        row, col = position
        points = [
            ((row + 1, col), (row - 1, col)),
            ((row, col + 1), (row, col - 1)),
            ((row - 1, col), (row + 1, col)),
            ((row, col - 1), (row, col + 1)),
        ]
        possible_player_points = []
        for player_position, opposite_point in points:
            if not self.isInBoard(player_position):
                continue
            if not self.isInBoard(opposite_point):
                continue
            if self.getBlock(opposite_point).has_a_rock():
                continue
            if not self.getBlock(player_position).get_is_walkable():
                continue
            if not self.getBlock(opposite_point).can_contain_rock():
                if not self.getBlock(opposite_point).get_is_walkable():
                    continue
            possible_player_points.append(player_position)
        return possible_player_points

    def generateBoard(self, gameMap, gameBoard):
        """
        Generates the board based on the given map
        """
        self.board = []
        generator = BlockGenerator(gameBoard)
        # generate an empty matrix with the same size as the map
        for row in range(len(gameMap)):
            self.board.append([])
            for col in range(len(gameMap[row])):
                self.board[row].append(None)

        # generate the board
        for row in range(len(gameMap)):
            for col in range(len(gameMap[row])):
                self.board[row][col] = generator.generate(gameMap[row][col])
                # update player location
                if gameMap[row][col] == 'P':
                    self.characterLocation = (row, col)
                # Update arrival location
                if gameMap[row][col] == 'A':
                    self.destinationLocation = (row, col)
                # update diamonds
                if gameMap[row][col] == 'D':
                    self.remainingDiamonds += 1
                # update visited blocks if is a rock
                if gameMap[row][col] == 'R':
                    self.board[row][col].get_rock().visit((row, col))
                # add the locaation
                self.board[row][col].set_location((row, col))
        return self.board

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

        # convert the reachable blocks to a list of ReachableBlock
        reachableBlocksList = []
        for blocks, path in reachableBlocks.items():
            block_from, block_to = blocks
            reahableBlock = ReachableBlock(block_from, block_to, path)
            reachableBlocksList.append(reahableBlock)

        # sort the list based on the lenght of the path
        reachableBlocksList.sort(key=lambda x: x.distance)
        return reachableBlocksList

    def getSpecialBlocksRecursive(self, location, visited, reachableBlocks, path):
        """
        Recursive function to get all the special blocks that are reachable from the given location

        Parameters
        ----------
        location : Tuple(Int)
            The location to start from
        visited : List(List(Bool))
            A matrix of the same size as the board, but filled with False
        reachableBlocks : Dict(BlockIterface, List(Tuple(Int)))
            A list of all the reachable blocks
        path : List(Tuple(Int))
            The path to the current location

        Returns
        -------
        Dict(BlockIterface, List(Tuple(Int)))
        """

        # get the current block
        block = self.getBlock(location)
        curr_row, curr_col = location

        def _updateReachableBlocks(blockFrom, BlockTo):
            """
            Updates the reachable blocks list
            """
            if (blockFrom, BlockTo) not in reachableBlocks:
                reachableBlocks[(blockFrom, BlockTo)] = copy.deepcopy(path)
            elif len(path) < len(reachableBlocks[(blockFrom, BlockTo)]):
                reachableBlocks[(blockFrom, BlockTo)] = copy.deepcopy(path)

        # if the current block is a special block, add it to the reachable blocks
        if block.isReachable():
            # save a tuple with the first postion current block and the second position next block
            if block.get_is_collectable():
                _updateReachableBlocks(block, block)
                return

            close_rocks = block.get_close_rocks()

            for rock in close_rocks:
                _updateReachableBlocks(block, rock)

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
        returns a list of neighbors of the given location, the neighbords are tuples of (row, col) of blocks that are walkable
        Parameters
        ----------
        location : Tuple(Int)
            The location to get the neighbors from
        visited : List(List(Bool))
            A matrix of the same size as the board, but filled with False
        Returns
        -------
        List(Tuple(Int))
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
        neighbors = [neighbor for neighbor in neighbors if self.board[neighbor[0]][neighbor[1]].get_is_walkable()]

        return neighbors

    def __str__(self) -> str:
        map_str = ""
        for row in self.board:
            for block in row:
                if block.has_a_rock():
                    map_str += "R"
                elif self.characterLocation == block.get_position():
                    map_str += "P"
                elif isinstance(block, Diamond):
                    if block.get_is_collectable():
                        map_str += "D"
                    else:
                        map_str += "F"
                else:
                    map_str += str(block)
                map_str += " "
            map_str += "\n"
        return map_str

    def get_new_rock_location(self, character_location_block, rock_location_block):
        """
        Returns the new location of the rock after moving it in the given direction
        Parameters
        ----------
        character_location_block : BlockInterface
            The block that the character is on
        rock_location_block : BlockInterface
            The block that the rock is on
        """

        direction = getDirectionOfMovement(character_location_block.get_position(), rock_location_block.get_position())
        row, col = rock_location_block.get_position()
        if direction == "L":
            col -= 1
        elif direction == "R":
            col += 1
        elif direction == "U":
            row -= 1
        elif direction == "D":
            row += 1
        return self.getBlock((row, col))

    def moverRock(self, character_location_block, rock_location_block):
        """
        Taking the character location and the rock location, move the rock to oposite direction of the character
        Parameters
        ----------
        character_location_block : BlockInterface
            The block where the character is located
        rock_location_block : BlockInterface
            The block where the rock is located
        """
        # get the new rock position after the movement
        new_rock_location_block = self.get_new_rock_location(character_location_block, rock_location_block)

        # move the rock
        rock = rock_location_block.get_rock()  # take the rock from the rock location
        new_rock_location_block.set_rock(rock)  # add the rock to the new rock location
        rock.visit(new_rock_location_block.get_position())  # update the visited matrix from the rock
        rock_location_block.set_rock(None)  # remove the rock form the rock location
        return new_rock_location_block

    def moveBackRock(self, character_location_block, rock_location_block):
        """
        Taking the character location and the rock location, move the rock to oposite direction of the character
        Parameters
        ----------
        character_location_block : BlockInterface
            The block where the character is located
        rock_location_block : BlockInterface
            The block where the rock is located
        """
        # get the new rock position after the movement
        new_rock_location_block = self.get_new_rock_location(character_location_block, rock_location_block)
        # move the rock
        rock = new_rock_location_block.get_rock()  # take the rock from the rock location
        new_rock_location_block.set_rock(None)  # remove the rock form the rock location
        rock_location_block.set_rock(rock)  # add the rock to the new rock location
        rock.unVisit(new_rock_location_block.get_position())  # update the visited matrix from the rock

    def moveBack(self, reachableBlock, step):
        """
        Moves the character back to the given block reverting the changes made to the board
        """
        if reachableBlock.block_from == reachableBlock.block_to:
            # interact with the las element of the path
            reachableBlock.block_from.unInteract(step)

            # change the character location
            path = reachableBlock.path
            self.characterLocation = path[0]

            # unwalk over the path between the character and the block
            for i in range(1, len(path) - 1):
                row_point = path[i][0]
                col_point = path[i][1]
                self.board[row_point][col_point].unwalkOver()
        else:
            # unInteract wiht the last element of the path
            reachableBlock.block_to.unInteract(step)
            # unMove the rock
            self.moveBackRock(reachableBlock.block_from, reachableBlock.block_to)
            path = reachableBlock.path
            self.characterLocation = path[0]

    def moveTo(self, reachableBlock, step):
        """
        Moves the character to the given block

        Parameters:
        ----------
        reachableBlock : ReachableBlock
            the block to move to, its compossed by an array of points of the map where the character moves
            for example: [(3, 3), (2, 3), (1, 3), (0, 3)] it means that the character moves from (3, 3) to (0, 3)
            incluiding the block (0, 3) in the path
        """
        if reachableBlock.block_from == reachableBlock.block_to:
            # interact wiht the last element of the path
            reachableBlock.block_from.interact(step)
            # move the character
            self.characterLocation = reachableBlock.block_from.get_position()
            # move the blocks
            path = reachableBlock.path
            for i in range(1, len(path) - 1):
                row_point = path[i][0]
                col_point = path[i][1]
                self.board[row_point][col_point].walkOver()
            # get the list of moves
            return reachableBlock.list_movements

        else:
            # move the rock
            self.moverRock(reachableBlock.block_from, reachableBlock.block_to)
            # interact wiht the last element of the path
            reachableBlock.block_to.interact(step)
            # move the character
            self.characterLocation = reachableBlock.block_to.get_position()

            # move the blocks
            path = reachableBlock.path
            for i in range(1, len(path)):
                row_point = path[i][0]
                col_point = path[i][1]
                self.board[row_point][col_point].walkOver()
            # get the list of moves
            list_movements = reachableBlock.list_movements
            # add the movement result of moving the rock
            list_movements.append(getDirectionOfMovement(reachableBlock.block_from.get_position(),
                                                         reachableBlock.block_to.get_position()))
            return list_movements

    def getShortestSolutionPath(self):
        """
        Returns the shortest path to the solution
        This path should collect all the diamonds
        """
        instructions = []
        visited = {}
        step = 1
        self.getSinlgeSolutionPathRecursive(instructions, visited, step)
        # self.getBestSolutionPathRecursive(instructions, best_instructions)
        return instructions

    def getSinlgeSolutionPathRecursive(self, instructions, visited, step):
        """
        Recursive function to get the shortest path to the solution
        """
        # if the character is alrady at the destination, return an empty list
        if self.isSolved():
            return True
        # get the reachable blocks
        reachableBlocks = self.getSpecialBlocksPath()

        # for each reachable block, move to it and call the function recursively
        for i, ReachableBlock in enumerate(reachableBlocks):
            list_movements = self.moveTo(ReachableBlock, step)
            instructions.extend(list_movements)
            # call the function recursively
            if self.getSinlgeSolutionPathRecursive(instructions, visited, step + 1):
                return True
            # move back
            self.moveBack(ReachableBlock, step)
            # remove the moves from the instructions
            for _ in range(len(list_movements)):
                instructions.pop()

        return False

    def getShortestPathFromTo(self, from_location, to_locations):
        """
        Returns the shortest path from the given location to the given location
        Parameters
        ----------
        from_location : tuple
            The location from where the path starts
        to_locations : list
            The list of locations where the path ends
        """
        visited = self.generateVisitedMatrix()
        visited[from_location[0]][from_location[1]] = 1
        path = [from_location]
        shortest_path = {}
        self.getShortestPathFromToRecursive(from_location, to_locations, visited, path, shortest_path)
        return shortest_path

    def getShortestPathFromToRecursive(self, from_location, to_locations, visited, path, shortest_path):
        """
        Recursive function to get the shortest path from the given location to the given location
        Parameters
        ----------
        from_location : tuple
            The location from where the path starts
        to_locations : list
            The list of locations where the path ends
        visited : list
            The matrix of visited blocks
        path : list
            The path from the start to the current block
        shortest_path : list
            The shortest path from the start to the current block
        """
        # if the character is alrady at the destination, return an empty list
        if from_location in to_locations:
            if from_location not in shortest_path:
                shortest_path[from_location] = copy.deepcopy(path)
            else:
                if len(path) < len(shortest_path[from_location]):
                    shortest_path[from_location] = copy.deepcopy(path)

        # get neighbors
        neighbors = self.getNeighbors(from_location, visited)
        # for each neighbor, move to it and call the function recursively
        for row, col in neighbors:
            if not visited[row][col]:
                visited[row][col] = True
                path.append((row, col))
                self.getShortestPathFromToRecursive((row, col), to_locations, visited, path, shortest_path)
                path.pop()
                visited[row][col] = False

    def getSpecialBlocksPathsWithRock(self, rock):
        """
        Returns the list of reachable blocks from the current location of the character the reachable blocks are holes or buttons
        Parameters
        ----------
        rock : Rock
            The rock to move
        """
        # get the reachable blocks
        reachableBlocks = self.getSpecialBlocksPath()
        # filter the reachable blocks
        reachableBlocks = list(filter(lambda x: x.block_from == rock or x.block_to == rock, reachableBlocks))
        return reachableBlocks

    def isInBoard(self, point):
        """
        Checks if the given point is in the board
        """
        rows = len(self.board)
        cols = len(self.board[0])
        return point[0] >= 0 and point[0] < rows and point[1] >= 0 and point[1] < cols
