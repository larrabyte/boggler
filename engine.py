import terminal as term
import random as rand
import typing as t
import data as dt
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
        self.hp = health
        self.attacks = []

    @property
    def health(self) -> int:
        return self.hp

    @health.setter
    def health(self, hp: int) -> None:
        # Ensure that health can't go below zero.
        self.hp = hp if hp >= 0 else 0

    def addattack(self, name: str, basedmg: int) -> None:
        # Add an attack to the character's attack dictionary.
        entry = (name, basedmg)
        self.attacks.append(entry)

    def randattack(self) -> t.Tuple[str, int]:
        # Return a random attack in a tuple of name/damage.
        name, damage = rand.choice(self.attacks)
        randomiser = rand.uniform(0.5, 1.5)
        return (name, int(damage * randomiser))

class Room:
    def __init__(self, name: str) -> None:
        self.name = name
        self.engaged = None
        self.enemies = []
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
        self.player = None
        self.terminal = None
        self.cursor = None
        self.dispatch = {}

    def battle(self) -> None:
        # Engage in a battle with an enemy in the room pointed to by the engine cursor.
        self.cursor.engaged = self.cursor.enemies.pop(0)

        def status() -> None:
            self.terminal.clear()
            self.terminal.print(dt.header)
            self.terminal.print(f"{self.cursor.engaged.name}: {self.cursor.engaged.health}HP")
            self.terminal.print(f"{self.player.name}: {self.player.health}HP\n")

        status()
        self.terminal.typeout("Uh-oh, looks like you ran into another enemy!\n", wpm=200)
        self.terminal.typeout("What shall you do?\n\n", wpm=200)

        while (action := self.terminal.getline()) is not None:
            response = self.interpret(mode="battle", userinput=action)

            self.terminal.clear()
            status()
            self.terminal.print(f"{response}\n")

            # If health is zero, exit the terminal and print aftermath.
            if self.cursor.engaged.health == 0:
                break

        self.terminal.print(f"You beat {self.cursor.engaged}!\n")

    def interpret(self, mode: str, userinput: str) -> str:
        # Use a dispatch table to run the correct function.
        # Don't try and interpret input that consists of whitespace.
        if len(argv := userinput.split()) == 0:
            return

        table = self.dispatch[mode]
        if (func := table.get(argv[0], None)) is not None:
            result = func(self, argv[1:])
            return result

        return f"bosh: command not found: {argv[0]}"
