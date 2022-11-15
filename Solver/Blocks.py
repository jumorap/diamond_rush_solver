class BlockInterface:
    def __init__(self, is_collectable, is_movable, is_walkable, name, gameBoard):
        #document the block
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
        
        self.is_collectable = is_collectable
        self.is_movable = is_movable
        self.is_walkable = is_walkable 
        self.name = name
        self.gameBoard = gameBoard

    def walkOver(self):
        pass

    def unwalkOver(self):
        pass

    def isReachable(self):
        return False

    def set_is_collectable(self, is_collectable):
        self.is_collectable = is_collectable
    
    def set_is_movable(self, is_movable):
        self.is_movable = is_movable

    def set_is_walkable(self, is_walkable):
        self.is_walkable = is_walkable

    def get_gameBoard(self):
        return self.gameBoard

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
        super().__init__(False, False, True, "Destination", gameBoard)

    def isReachable(self):
        #if there is no more diamonds to collect, the destination is reachable
        return super().get_gameBoard().remainingDiamonds == 0

class Key(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Key", gameBoard)

    def isReachable(self):
        return True

class Diamond(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(True, False, True, "Diamond", gameBoard)
    
    def isReachable(self):
        return True

class KeyDoor(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "KeyDoor", gameBoard)
    
    def isReachable(self):
        return super().get_gameBoard().currentKeys > 0

class Spikes(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, False, False, "Spikes", gameBoard)

    def walkOver(self):
        pass

class Rock(BlockInterface):
    def __init__(self, gameBoard):
        super().__init__(False, True, True, "Rock", gameBoard)

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
