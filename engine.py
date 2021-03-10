import random
import time
import sys

def slowtype(message: str, speed: float) -> None:
    """Print characters like a typewriter."""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        cps = random.random() * 12 / speed
        time.sleep(cps)
