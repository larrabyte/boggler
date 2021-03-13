from __future__ import annotations
from enum import Enum
import typing as t

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
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
        self.links = {
            Direction.NORTH: None,
            Direction.EAST: None,
            Direction.WEST: None,
            Direction.SOUTH: None
        }

    def adjacent(self) -> t.Generator[Room]:
        """Return a generator for iterating over each adjacent room."""
        for key, value in self.links.items():
            if value is None: continue
            yield (key, value)

    def link(self, direction: Direction, destination: Room) -> None:
        """Link two rooms together, adding entries to both objects."""
        self.links[direction] = destination
        destination.links[direction.opposite] = self

    def unlink(self, direction: Direction) -> None:
        """Unlinks two rooms, making sure to destroy both references in both directions."""
        if (entry := self.links[direction]) is not None:
            entry.links[direction.opposite] = None
            self.links[direction] = None

class Character:
    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.inventory = []

class Engine:
    def __init__(self) -> None:
        self.player = Character(name="Player", health=100)
        self.cursor = None
