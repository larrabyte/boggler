import importlib
import random
import time
import sys
import os

class Terminal:
    def __init__(self) -> None:
        if os.name != "nt":
            self.termios = importlib.import_module("termios")
            self.tty = importlib.import_module("tty")
            self.getchar = self.getunixchar
            self.clearer = "clear"
        else:
            self.msvcrt = importlib.import_module("msvcrt")
            self.getchar = self.msvcrt.getwch
            self.clearer = "cls"

        self.clear()

    def clear(self) -> None:
        # Clears the terminal using system-specific calls.
        os.system(self.clearer)

    def print(self, message: str, **kwargs: dict) -> None:
        # Print a string to the terminal.
        print(message, **kwargs)

    def typeout(self, message: str, wpm: int) -> None:
        # Type out characters to the terminal.
        for char in message:
            print(char, end="", flush=True)
            cps = 8 / wpm
            time.sleep(cps)

    def getunixchar(self) -> None:
        # Run UNIX-specific code to grab a character from standard input.
        fd = sys.stdin.fileno()
        settings = self.termios.tcgetattr(fd)

        try:
            self.tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            when = self.termios.TCSADRAIN
            self.termios.tcsetattr(fd, when, settings)

        return ch

    def getline(self) -> str:
        # Return input from the terminal.
        self.print("$ ", end="", flush=True)
        forbidden = "\x7f\x0d\x1b"
        buffer = ""
        cursor = 0

        while (char := self.getchar()):
            # Are we able to print out this character?
            if char not in forbidden:
                self.print(char, end="", flush=True)
                buffer += char
                cursor += 1

            # If the user backspaces, move the cursor back.
            elif char == "\x7f" and cursor > 0:
                self.print("\b \b", end="", flush=True)
                buffer = buffer[:-1]
                cursor -= 1

            # Break this loop if the user presses Enter.
            elif char == "\x0D":
                break

        self.print("\n", end="", flush=True)
        return buffer
