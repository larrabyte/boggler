import typing as t
import enum as e

class Direction(e.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def fromstr(string: str) -> t.Optional[object]:
        # Get a direction object representing the string's direction.
        if string.lower() == "north":
            return Direction.NORTH
        elif string.lower() == "east":
            return Direction.EAST
        elif string.lower() == "south":
            return Direction.SOUTH
        elif string.lower() == "west":
            return Direction.WEST

        return None

    @property
    def opposite(self) -> object:
        # Return the opposite direction of itself.
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.SOUTH:
            return Direction.NORTH

        return Direction.EAST

class Character:
    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.inventory = []

class Room:
    def __init__(self, name: str) -> None:
        self.name = name
        self.enemies = []
        self.drops = []
        self.links = {
            Direction.NORTH: None,
            Direction.EAST: None,
            Direction.SOUTH: None,
            Direction.WEST: None
        }

    def adjacent(self) -> str:
        # Generate a printable string showing this room's current surroundings.
        north = getattr(self.links[Direction.NORTH], "name", None) or "END"
        east = getattr(self.links[Direction.EAST], "name", None) or "END"
        south = getattr(self.links[Direction.SOUTH], "name", None) or "END"
        west = getattr(self.links[Direction.WEST], "name", None) or "END"

        # Calculate the necessary spacing to get the text centred on the dot.
        horizontal = f"  {west} -- W -- ● -- E -- {east}"
        spacing = horizontal.index("●") * 2 + 1

        # Add the text to one giant string before returning.
        formatted = f"\n{north.center(spacing)}\n"
        formatted += f"{'|'.center(spacing)}\n{'N'.center(spacing)}\n{'|'.center(spacing)}\n"
        formatted += f"{horizontal}\n"
        formatted += f"{'|'.center(spacing)}\n{'S'.center(spacing)}\n{'|'.center(spacing)}"
        formatted += f"\n{south.center(spacing)}"
        return formatted

    def link(self, direction: Direction, destination: object) -> None:
        # Link two rooms together, adding entries to both objects.
        self.links[direction] = destination
        destination.links[direction.opposite] = self

    def unlink(self, direction: Direction) -> None:
        # Unlinks two rooms, making sure to destroy both references in both directions.
        if (entry := self.links[direction]) is not None:
            entry.links[direction.opposite] = None
            self.links[direction] = None

class Engine:
    def __init__(self) -> None:
        self.player = Character(name="Player", health=100)
        self.dispatch = {}
        self.cursor = None

    def interpret(self, argv: t.List[str]) -> str:
        # Interpret a string passed in from the player.
        # Uses the dispatch table to run the correct function.
        if (func := self.dispatch.get(argv[0], None)) is not None:
            result = func(self, argv[1:])
            return result

        return f"bosh: command not found: {argv[0]}"
