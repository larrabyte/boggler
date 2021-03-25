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
    mmu = en.Room("Memory Management Unit")
    cache = en.Room("Memory Cache")
    apic = en.Room("Interrupt Controller")
    ram = en.Room("Random Access Memory")
    pcie = en.Room("PCI Express Bus")
    hdd = en.Room("Hard Disk Drive")
    sb = en.Room("South Bridge")
    fpu = en.Room("Floating Point Unit")
    gpu = en.Room("Graphics Processing Unit")
    ethernet = en.Room("Ethernet Adapter")
    www = en.Room("The World Wide Web")
    ssd = en.Room("Solid State Drive")
    chipset = en.Room("Chipset")
    io = en.Room("I/O Hub")
    speaker = en.Room("PC Speaker")

    # Link all the rooms together.
    cpu.link(en.Direction.NORTH, fpu)
    cpu.link(en.Direction.EAST, mmu)
    cpu.link(en.Direction.SOUTH, sb)
    cpu.link(en.Direction.WEST, apic)
    mmu.link(en.Direction.NORTH, cache)
    mmu.link(en.Direction.SOUTH, ram)
    sb.link(en.Direction.EAST, pcie)
    sb.link(en.Direction.WEST, io)
    sb.link(en.Direction.SOUTH, chipset)
    io.link(en.Direction.NORTH, ssd)
    io.link(en.Direction.WEST, hdd)
    io.link(en.Direction.SOUTH, ethernet)
    ethernet.link(en.Direction.WEST, www)
    chipset.link(en.Direction.EAST, speaker)
    pcie.link(en.Direction.NORTH, gpu)
    instance.cursor = cpu
    instance.goal = www

    # Add enemies to each room.
    bigman = en.Character(name="ethernet device driver", health=75)
    bigman.addattack(name="tcp/ip stack", basedmg=50)
    bigman.addattack(name="the power of cryptography", basedmg=50)
    bigman.addattack(name="nsa backdoor", basedmg=200)
    bigman.addattack(name="endianness", basedmg=25)
    ethernet.enemies.append(bigman)

    southman = en.Character(name="the gatekeeper of the south", health=20)
    southman.addattack(name="ring 0 access only", basedmg=10)
    southman.addattack(name="sike smm interrupt", basedmg=20)
    southman.addattack(name="raise interrupt 13", basedmg=15)
    sb.enemies.append(southman)

    ioman = en.Character(name="stuxnet", health=75)
    ioman.addattack(name="throw centrifuges", basedmg=25)
    ioman.addattack(name="lay dormant", basedmg=0)
    ioman.addattack(name="become siemens", basedmg=25)
    ioman.addattack(name="corrupt disk", basedmg=50)
    io.enemies.append(ioman)

    final = en.Character(name="the onion router", health=200)
    final.addattack(name="onions", basedmg=999)
    final.addattack(name="anonymous traffic spammer", basedmg=25)
    final.addattack(name="unknown silky substances", basedmg=25)
    final.addattack(name="third-party routing software", basedmg=25)
    final.addattack(name="ethereum miner", basedmg=25)
    final.addattack(name="deep packet inspection", basedmg=25)
    final.addattack(name="man in the middle attack", basedmg=25)
    final.addattack(name="isp throttling", basedmg=25)
    www.enemies.append(final)

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

        if engine.cursor == engine.goal:
            # We won the game.
            size = len(dt.header.split("\n")[0])
            engine.terminal.print("YOU WIN".center(size))
            engine.terminal.print("GG EZ".center(size))
            engine.terminal.print("")
            break
