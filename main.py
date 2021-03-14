import terminal as term
import engine as en
import maps
import data
import time

if __name__ == "__main__":
    engine = en.Engine()
    engine.cursor = maps.setupmap()

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
    print("---------------------------------------------\n")
    term.getchar("Press any key to quit.")
