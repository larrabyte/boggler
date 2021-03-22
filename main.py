import terminal as term
import commands as cmd
import engine as en
import typing as t
import data as dt

import inspect
import time
import sys

def completeinit(instance: en.Engine, playername: str, atkname: str) -> None:
    # Final engine initialisation. All rooms are created,
    # items and enemies assigned and initial spawn room set.
    instance.player = en.Character(name=playername, health=100)
    instance.player.addattack(name=atkname, basedmg=10)

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

def getnames() -> t.Tuple[str, str]:
    # Print the initial screen and query for player data.
    screen.clear()
    screen.print(dt.header)
    screen.typeout("What is your name?\n", wpm=200)

    while (playername := screen.getline()) is not None:
        # If we have a valid name, break out of this loop.
        if not playername.isspace() and playername != "":
            break

        screen.print("\nInvalid name. Try another!")
        screen.print("What is your name?")

    screen.clear()
    screen.print(dt.header)
    screen.typeout("What should your first attack be called?\n", wpm=200)

    while (atkname := screen.getline()) is not None:
        # If we have a valid name, break out of this loop.
        if not atkname.isspace() and atkname != "":
            break

        screen.print("\nInvalid name. Try another!")
        screen.print("What should your first attack be called?")

    return (playername, atkname)

if __name__ == "__main__":
    engine = en.Engine()
    screen = term.Terminal()
    engine.terminal = screen

    if len(sys.argv) != 2 or sys.argv[1] != "skip":
        # Print a fake bootsplash if no skip command was issued.
        bootsplash(engine)

    # Finish initialisation of the game engine.
    playername, atkname = getnames()
    completeinit(engine, playername, atkname)

    screen.clear()
    screen.print(dt.header)
    screen.typeout("You look around and see bits flying in all directions.\n", wpm=200)
    screen.typeout("You hear the incessant ticking of the CPU clock, whirring along at billions of cycles per second.\n", wpm=200)
    screen.typeout("You just might be inside a computer.\n\n", wpm=200)

    while (userinput := screen.getline()) is not None:
        # Don't try and interpret input that consists of whitespace.
        if userinput.isspace(): continue

        # Split the input into words and send to the engine.
        userinput = userinput.split()
        response = engine.interpret(userinput)
        screen.print(f"{response}\n")
