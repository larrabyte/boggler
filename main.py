import terminal as term
import commands as cmd
import engine as en

import inspect
import data
import time
import sys

def completeinit(instance: en.Engine) -> None:
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

    # Fill the dispatch table with commands.
    funky = {k:v for k, v in inspect.getmembers(cmd, inspect.isfunction)}
    instance.dispatch.update(funky)

def bootsplash() -> None:
    # Print a boot sequence to standard out.
    term.clear()
    term.typeout(data.initial, speed=300)
    term.typeout(data.bootstrap, speed=25000)
    time.sleep(0.25)
    term.typeout(data.final1, speed=50000)
    time.sleep(1)
    term.typeout(data.final2, speed=50000)
    time.sleep(2)
    term.typeout(data.final3, speed=50000)
    time.sleep(2)

if __name__ == "__main__":
    engine = en.Engine()
    completeinit(engine)

    if len(sys.argv) != 2 or sys.argv[1] != "skip":
        bootsplash()

    term.clear() # Clear the screen and start the terminal.
    print("---------------------------------------------")
    print("larrabyte/boggler: a text-adventure RPG game.")
    print("---------------------------------------------")
    print("something something put some text here to introduce the player to the game.")
    print("tl;dr you're inside a computer.\n")

    while (userinput := input("$ ")) != "":
        userinput = userinput.split()
        response = engine.interpret(userinput)
        print(f"{response}\n")
