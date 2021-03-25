import random as rand
import typing as t
import data as dt
import enum as e
import sys as s

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
        self.goal = None
        self.dispatch = {}

    def battle(self) -> None:
        # Engage in a battle with an enemy in the room pointed to by the engine cursor.
        self.cursor.engaged = self.cursor.enemies.pop(0)

        def header() -> str:
            size = len(dt.header.split("\n")[0])
            text = dt.header

            text += f"\n{'BATTLE MODE ACTIVE'.center(size)}\n"
            text += f"{self.cursor.engaged.name} vs. {self.player.name}".center(size) + "\n"
            text += f"{self.cursor.engaged.health}HP to {self.player.health}HP".center(size) + "\n"
            return text

        # Print the battle header.
        self.terminal.clear()
        self.terminal.print(header())
        self.terminal.typeout("Uh-oh, looks like you ran into another enemy!\n", wpm=200)
        self.terminal.typeout("What shall you do?\n\n", wpm=200)

        # Let the user decide the course of action to take.
        while (action := self.terminal.getline()) is not None:
            response = self.interpret(mode="battle", userinput=action)

            # If the cursor is none, then the battle has been stopped!
            if self.cursor.engaged is None:
                return

            self.terminal.clear()
            self.terminal.print(header())
            self.terminal.print(f"{response}\n")

            # If health is zero, exit the terminal and print aftermath.
            if self.cursor.engaged.health == 0:
                break

            # Check the user's health after the enemy.
            # If both hit zero, then let the user "win".
            if self.player.health == 0:
                size = len(dt.header.split("\n")[0])
                self.terminal.print("YOU DIED".center(size))
                self.terminal.print("")
                s.exit()

        # If we reach this point, then the user has beaten the user.
        self.terminal.print(f"You managed to beat {self.cursor.engaged.name}!")
        self.terminal.print(f"It seems they left behind these attacks:")

        for index, attack in enumerate(self.cursor.engaged.attacks):
            self.terminal.print(f"    {index}. {attack[0]} (base damage of {attack[1]})")

        # Convert their attacks to a dictionary for ease of lookup.
        self.terminal.print("\nWhich one would you like to pickup? If you don't wish to pick up anything, type \"none\".\n")
        conversion = {str(k): v for k, v in enumerate(self.cursor.engaged.attacks)}

        while (wanted := self.terminal.getline()) is not None:
            if (attack := conversion.get(wanted, None)) is not None:
                self.player.addattack(name=attack[0], basedmg=attack[1])
                self.terminal.typeout(f"You learnt how to attack with {attack[0]}!\n", wpm=200)
                break
            elif wanted == "none":
                self.terminal.typeout(f"You watch as the body of {self.cursor.engaged.name} slowly fades out of existence.\n", wpm=200)
                break

        self.terminal.typeout(f"The sounds of battle echo throughout the room.\n\n", wpm=200)
        self.player.health = 100

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
