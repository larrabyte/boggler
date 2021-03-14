import terminal as term
import engine as en
import data
import time
import sys

if __name__ == "__main__":
    engine = en.Engine()
    engine.mapsetup()

    if len(sys.argv) > 1 and sys.argv[1] == "skip":
        # Don't show the boot screen if the user wants to skip.
        pass
    else:
        term.clear()
        term.typeout(data.Booter.initial, speed=300)
        term.typeout(data.Booter.bootstrap, speed=25000)
        time.sleep(0.25)
        term.typeout(data.Booter.final1, speed=50000)
        time.sleep(1)
        term.typeout(data.Booter.final2, speed=50000)
        time.sleep(2)
        term.typeout(data.Booter.final3, speed=50000)
        time.sleep(2)

    term.clear()
    print("---------------------------------------------")
    print("larrabyte/boggler: a text-adventure RPG game.")
    print("---------------------------------------------")
    print("something something put some text here to introduce the player to the game.")
    print("tl;dr you're inside a computer.\n")

    while (userinput := input("$ ")) != "":
        userinput = userinput.split()
        response = engine.interpret(userinput)
        print(f"{response}\n")
