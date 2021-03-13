from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Room:
    def __init__(self, name: str) -> None:
        self.name = name
        self.enemies = []
        self.drops = []
        self.links = {}

    def link(self, direction: Direction, destination: object) -> None:
        """Link two rooms together, adding entries to both objects."""
        self.links[direction] = destination
        destination.links[direction - 2] = self

class Character:
    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.inventory = []

class Engine:
    def __init__(self) -> None:
        self.player = Character(name="Player", health=100)
        self.rooms = []
