import terminal as term
import engine as en
import typing as t

import sys

def help(ctx: en.Engine, arguments: t.List[str]) -> str:
    return "No one will help you here."

def whereami(ctx: en.Engine, arguments: t.List[str]) -> str:
    return ctx.cursor.adjacent()

def clear(ctx: en.Engine, arguments: t.List[str]) -> str:
    term.clear()

    return ("---------------------------------------------\n"
            "larrabyte/boggler: a text-adventure RPG game.\n"
            "---------------------------------------------")

def exit(ctx: en.Engine, arguments: t.List[str]) -> str:
    sys.exit()

def go(ctx: en.Engine, arguments: t.List[str]) -> str:
    if len(arguments) >= 1 and (direction := en.Direction.fromstr(arguments[0])) is not None:
        if (room := ctx.cursor.links[direction]) is not None:
            ctx.cursor = room
            return f"Moved {arguments[0]} to {ctx.cursor.name}."
        else:
            return "There isn't a room in that direction."

    return f"Where are you going to go?"
