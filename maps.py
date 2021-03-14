import engine as en

def setupmap() -> en.Room:
    """Setup the map as defined in this function."""
    cpu = en.Room("Central Processing Unit")
    ram = en.Room("Random Access Memory")
    sb = en.Room("South Bridge")
    mb = en.Room("Motherboard")

    cpu.link(en.Direction.SOUTH, sb)
    cpu.link(en.Direction.EAST, ram)
    sb.link(en.Direction.SOUTH, mb)

    return cpu
