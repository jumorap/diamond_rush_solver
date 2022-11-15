import Blocks as Blocks

class BlockGenerator:
    """
    Class to generate all the objects based on a fixed map
    """
    def __init__(self):
        self.map = {
            'R' :  Blocks.Rock,
            'D' : Blocks.Diamond,
            'P' : "",
            'M' : Blocks.Wall,
            'W' : Blocks.Magma,
            'A' : Blocks.Destination,
            'C' : Blocks.Floor,
            'K' : Blocks.KeyDoor,
            'L' : Blocks.Key,
            'S' : Blocks.Spikes,
            'H' : Blocks.Hole,
            'B' : Blocks.Button,
            'U' : Blocks.DoorButton,
        }

    def generate(self, target):
        """
        returns a new Object based on the given char
        for example:
        'R' -> Rock
        'D' -> Diamond
        """
        return  self.map[target]()
