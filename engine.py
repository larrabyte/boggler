from __future__ import annotations
from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self) -> Direction:
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.SOUTH:
            return Direction.NORTH

        return Direction.EAST

class Room:
    def __init__(self, name: str) -> None:
        self.name = name
        self.enemies = []
        self.drops = []
        self.links = {}

    def link(self, direction: Direction, destination: Room) -> None:
        """Link two rooms together, adding entries to both objects."""
        self.links[direction] = destination
        destination.links[direction.opposite()] = self

class Character:
    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.inventory = []

class Engine:
    def __init__(self) -> None:
        self.player = Character(name="Player", health=100)
        self.rooms = []
