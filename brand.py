# startup banner for the prodigy tools - by Zaphh-Tech
# shows the project name with a moving colour sweep. quiet when piped.

import sys
import time

C = {"reset": "\033[0m", "dim": "\033[2m", "base": "\033[38;5;44m",
     "glow": "\033[1;38;5;51m", "hot": "\033[1;97m", "accent": "\033[38;5;120m"}


def _tty():
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def boot(name, code, tagline=""):
    if not _tty():
        return
    name = name.upper()
    inner = max(len(name), len(f"PRODIGY {code}  -  by Zaphh-Tech"), len(tagline)) + 6
    top = "╔" + "═" * inner + "╗"
    bot = "╚" + "═" * inner + "╝"
    line2 = "   PRODIGY " + code + "  -  by Zaphh-Tech"
    rows = [top,
            "║" + " " * inner + "║",
            "║   " + name + " " * (inner - 3 - len(name)) + "║",
            "║" + line2 + " " * (inner - len(line2)) + "║",
            "║" + " " * inner + "║",
            bot]
    for r in rows:
        print(C["base"] + r + C["reset"])
    # moving light sweep across the box
    for pos in range(-3, inner + 5, 2):
        sys.stdout.write(f"\033[{len(rows)}A")
        for r in rows:
            out = []
            for i, ch in enumerate(r):
                d = abs(i - pos)
                col = C["hot"] if d <= 1 else C["glow"] if d <= 3 else C["base"]
                out.append(col + ch + C["reset"])
            sys.stdout.write("".join(out) + "\033[K\n")
        sys.stdout.flush()
        time.sleep(0.025)
    sys.stdout.write(f"\033[{len(rows)}A")
    for r in rows:
        sys.stdout.write(C["accent"] + r + C["reset"] + "\033[K\n")
    if tagline:
        print(C["dim"] + "   " + tagline + C["reset"])
    print()


if __name__ == "__main__":
    boot("Caesar Cipher", "CS-01", "classic shift cipher - encrypt / decrypt")
