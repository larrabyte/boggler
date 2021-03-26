import random as rand
import inspect as ins
import engine as en
import typing as t
import data as dt
import sys as s

class L1:
    @staticmethod
    def ls(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Shows currently adjacent rooms."""
        return ctx.cursor.adjacent()

    @staticmethod
    def clear(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Clear the terminal."""
        ctx.terminal.clear()
        return dt.header

    @staticmethod
    def exit(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Exit the game."""
        s.exit()

    @staticmethod
    def cd(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Head into another room given a direction."""
        if len(arguments) >= 1 and (direction := en.Direction.fromstr(arguments[0])) is not None:
            if (room := ctx.cursor.links[direction]) is not None:
                ctx.cursor = room
                return f"Moved {arguments[0]} to {ctx.cursor.name}."
            else:
                return "There isn't a room in that direction."

        return f"Where are you going to go?"

    @staticmethod
    def help(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Returns this help command."""
        functions = ins.getmembers(L1, ins.isfunction)
        strings = [f"{name}: {ptr.__doc__}" for name, ptr in functions]
        return "\n".join(strings)

class L2:
    @staticmethod
    def attack(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Attack the enemy, simple as that."""
        enemy = ctx.cursor.engaged
        pn, pd = ctx.player.randattack()
        en, ed = enemy.randattack()

        # Store temp enemy health to calculate difference.
        temp = enemy.health
        enemy.health -= pd
        enemydiff = temp - enemy.health

        temp = ctx.player.health
        ctx.player.health -= ed
        playerdiff = temp - ctx.player.health

        return (f"You dealt {enemydiff} damage to {enemy.name} using {pn}!\n"
                f"{enemy.name} dealt {playerdiff} damage to you using {en}!")

    @staticmethod
    def help(ctx: en.Engine, arguments: t.List[str]) -> str:
        """Returns this help command."""
        functions = ins.getmembers(L2, ins.isfunction)

        # Iterate over all functions available and store their name + docstring.
        strings = [f"{name}: {ptr.__doc__}" for name, ptr in functions]
        return "\n".join(strings)

    @staticmethod
    def flee(ctx: en.Engine, arguments: t.List[str]) -> t.Optional[str]:
        """Attempt to run away from the enemy."""
        if not ctx.cursor == ctx.goal and rand.randint(0, 100) > 75:
            # Give a 25% chance of escaping.
            ctx.cursor.engaged = None
            ctx.terminal.clear()
            ctx.terminal.print(dt.header)
            ctx.terminal.print("You managed to escape the battle.\n")
            return None

        return "No getting away this time!"
