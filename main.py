import terminal as term
import engine as en
import maps

if __name__ == "__main__":
    engine = en.Engine()
    engine.cursor = maps.setupmap()
    area = engine.cursor.adjacent()
    print(area)
