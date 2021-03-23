import terminal as term
import commands as cmd
import inspect as ins
import engine as en
import typing as t
import data as dt

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

    bootloader = en.Character(name="grubby bootloader", health=20)
    bootloader.addattack(name="invalid multiboot header", basedmg=5)
    bootloader.addattack(name="you must load the kernel first", basedmg=3)
    ram.enemies.append(bootloader)

    # Populate the dispatch table with commands.
    blueprint = {
        "normal": {k:v for k, v in ins.getmembers(cmd.L1, ins.isfunction)},
        "battle": {k:v for k, v in ins.getmembers(cmd.L2, ins.isfunction)}
    }

    instance.dispatch.update(blueprint)

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
    screen.typeout("System initialisation procedures.\n", wpm=200)
    screen.typeout("What is your name?\n\n", wpm=200)

    while (playername := screen.getline()) is not None:
        # If we have a valid name, break out of this loop.
        if not playername.isspace() and playername != "":
            break

        screen.print("Invalid name. Try another!\n")

    screen.clear()
    screen.print(dt.header)
    screen.typeout("System initialisation procedures.\n", wpm=200)
    screen.typeout("What should your first attack be called?\n\n", wpm=200)

    while (atkname := screen.getline()) is not None:
        # If we have a valid name, break out of this loop.
        if not atkname.isspace() and atkname != "":
            break

        screen.print("Invalid name. Try another!\n")

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
    screen.typeout("You awake to the sound of an alarm. Everything around you stands still as red light floods the room.\n", wpm=200)
    screen.typeout("The incessant ticking of the CPU clock ceases, casting a deafening silence over the whole building.\n", wpm=200)
    screen.typeout("As you get back on your feet, you notice a large crack along the eastern wall.\n", wpm=200)
    screen.typeout("What shall you do?\n\n", wpm=150)

    while (userinput := screen.getline()) is not None:
        if (response := engine.interpret(mode="normal", userinput=userinput)) is not None:
            screen.print(f"{response}\n")

        while len(engine.cursor.enemies) > 0:
            engine.battle()
