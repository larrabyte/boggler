import random
import time
import sys
import os

def clear() -> None:
    """Clears the terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def getchar(query: str) -> str:
    """Grabs a single character from standard input."""
    print(query)

    if os.name != "nt":
        # Run UNIX-specific code if we're not on Windows.
        import termios, tty, sys
        fd = sys.stdin.fileno()
        settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)
    else:
        # Otherwise, use getchar() from the Microsoft C runtime.
        from msvcrt import getwch
        ch = getwch()

    return ch

def typeout(message: str, speed: float) -> None:
    """Print characters like a typewriter."""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        cps = random.random() * 12 / speed
        time.sleep(cps)
