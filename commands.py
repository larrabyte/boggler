import terminal as term
import inspect as ins
import engine as en
import typing as t
import sys as s

def whereami(ctx: en.Engine, arguments: t.List[str]) -> str:
    """Shows currently adjacent rooms."""
    return ctx.cursor.adjacent()

def clear(ctx: en.Engine, arguments: t.List[str]) -> str:
    """Clear the terminal."""
    ctx.terminal.clear()

    return ("---------------------------------------------\n"
            "larrabyte/boggler: a text-adventure RPG game.\n"
            "---------------------------------------------")

def exit(ctx: en.Engine, arguments: t.List[str]) -> str:
    """Exit the game."""
    s.exit()

def cd(ctx: en.Engine, arguments: t.List[str]) -> str:
    """Head into another room given a direction."""
    if len(arguments) >= 1 and (direction := en.Direction.fromstr(arguments[0])) is not None:
        if (room := ctx.cursor.links[direction]) is not None:
            ctx.cursor = room
            return f"Moved {arguments[0]} to {ctx.cursor.name}."
        else:
            return "There isn't a room in that direction."

    return f"Where are you going to go?"

def ls(ctx: en.Engine, arguments: t.List[str]) -> str:
    """List enemies and drops available in this room."""
    return (f"Potential enemies: {ctx.cursor.enemies}\n"
            f"Potential drops: {ctx.cursor.drops}")

def help(ctx: en.Engine, arguments: t.List[str]) -> str:
    """Returns this help command."""
    functions = ins.getmembers(s.modules[__name__], ins.isfunction)
    strings = [f"{name}: {ptr.__doc__}" for name, ptr in functions]
    return "\n".join(strings)
