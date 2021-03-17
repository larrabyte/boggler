import terminal as term
import commands as cmd
import engine as en
import data as dt

import inspect
import string
import time
import sys

def completeinit(instance: en.Engine, screen: term.Terminal) -> None:
    # Final engine initialisation. All rooms are created,
    # items and enemies assigned and initial spawn room set.
    cpu = en.Room("Central Processing Unit")
    ram = en.Room("Random Access Memory")
    sb = en.Room("South Bridge")
    mb = en.Room("Motherboard")

    cpu.link(en.Direction.SOUTH, sb)
    cpu.link(en.Direction.EAST, ram)
    sb.link(en.Direction.SOUTH, mb)
    instance.cursor = cpu

    # Fill the dispatch table with commands and set the terminal instance.
    funky = {k:v for k, v in inspect.getmembers(cmd, inspect.isfunction)}
    instance.dispatch.update(funky)
    instance.terminal = screen

def bootsplash(engine: en.Engine) -> None:
    # Print a boot sequence to the terminal.
    engine.terminal.clear()
    engine.terminal.typeout(dt.initial, wpm=300)
    engine.terminal.typeout(dt.bootstrap, wpm=25000)
    time.sleep(0.25)
    engine.terminal.typeout(dt.final1, wpm=50000)
    time.sleep(1)
    engine.terminal.typeout(dt.final2, wpm=50000)
    time.sleep(2)
    engine.terminal.typeout(dt.final3, wpm=50000)
    time.sleep(2)

if __name__ == "__main__":
    engine = en.Engine()
    screen = term.Terminal()
    completeinit(engine, screen)

    if len(sys.argv) != 2 or sys.argv[1] != "skip":
        # Print a fake bootsplash if no skip command was issued.
        bootsplash(engine)

    screen.clear()
    screen.print("---------------------------------------------")
    screen.print("larrabyte/boggler: a text-adventure RPG game.")
    screen.print("---------------------------------------------")
    screen.print("something something put some text here to introduce the player to the game.")
    screen.print("tl;dr you're inside a computer.\n")

    while (userinput := screen.getline()) is not None:
        # Don't try and interpret input that consists of whitespace.
        if userinput.isspace(): continue

        # Split the input into words and send to the engine.
        userinput = userinput.split()
        response = engine.interpret(userinput)
        screen.print(f"{response}\n")
