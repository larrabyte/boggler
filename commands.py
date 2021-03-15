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
