import engine as en

def setupmap() -> en.Room:
    """Setup the map as defined in this function."""
    cpu = en.Room(name="Central Processing Unit")
    ram = en.Room(name="Random Access Memory")
    sb = en.Room(name="South Bridge")
    mb = en.Room(name="Motherboard")

    cpu.link(en.Direction.SOUTH, sb)
    cpu.link(en.Direction.EAST, ram)
    sb.link(en.Direction.SOUTH, mb)

    return cpu
