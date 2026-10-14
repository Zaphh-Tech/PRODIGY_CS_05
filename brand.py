# little startup banner for my prodigy tools - Zaphh-Tech
# shows an ascii logo with a moving light sweep, then the tool name.
# stays quiet when output isn't a real terminal (pipes/graders).

import sys
import time

LOGO = [
    "███████╗ █████╗ ██████╗ ██╗  ██╗██╗  ██╗",
    "╚══███╔╝██╔══██╗██╔══██╗██║  ██║██║  ██║",
    "  ███╔╝ ███████║██████╔╝███████║███████║",
    " ███╔╝  ██╔══██║██╔═══╝ ██╔══██║██╔══██║",
    "███████╗██║  ██║██║     ██║  ██║██║  ██║",
    "╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝",
    "   Z A P H H  -  T E C H   //  cyber    ",
]

C = {
    "reset": "\033[0m", "dim": "\033[2m", "base": "\033[38;5;44m",   # teal
    "glow": "\033[1;38;5;51m", "hot": "\033[1;97m", "accent": "\033[38;5;120m",
}


def _tty():
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def _slow(text, color, delay=0.012):
    for ch in text:
        sys.stdout.write(color + ch + C["reset"])
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def boot(tool, code, tagline=""):
    """Animated boot banner. No-op (prints nothing) on a non-tty."""
    if not _tty():
        return
    w = max(len(l) for l in LOGO)
    # 1. draw the logo once (base colour)
    for l in LOGO:
        print(C["base"] + l + C["reset"])
    # 2. moving light sweep: redraw in place with a bright column travelling
    for pos in range(-4, w + 6, 2):
        sys.stdout.write(f"\033[{len(LOGO)}A")           # cursor up to logo top
        for l in LOGO:
            out = []
            for i, ch in enumerate(l):
                if ch == " ":
                    out.append(" "); continue
                d = abs(i - pos)
                if d <= 1:
                    out.append(C["hot"] + ch + C["reset"])
                elif d <= 3:
                    out.append(C["glow"] + ch + C["reset"])
                else:
                    out.append(C["base"] + ch + C["reset"])
            sys.stdout.write("".join(out) + "\033[K\n")
        sys.stdout.flush()
        time.sleep(0.03)
    # 3. settle to accent colour
    sys.stdout.write(f"\033[{len(LOGO)}A")
    for l in LOGO:
        sys.stdout.write(C["accent"] + l + C["reset"] + "\033[K\n")
    # 4. tool line + msf-style init spinner
    bar = C["dim"] + "=" * w + C["reset"]
    print(bar)
    _slow(f"   [ {tool}  ·  PRODIGY {code} ]", C["glow"], 0.010)
    if tagline:
        _slow(f"   {tagline}", C["dim"], 0.006)
    spin = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    msg = "   [*] loading module"
    sys.stdout.write(C["accent"] + msg + C["reset"])
    sys.stdout.flush()
    for i in range(14):
        sys.stdout.write("\r" + C["accent"] + msg + " " + spin[i % len(spin)] + C["reset"])
        sys.stdout.flush()
        time.sleep(0.045)
    sys.stdout.write("\r" + C["accent"] + msg + " " + C["accent"] + "ready\033[K" + C["reset"] + "\n")
    print(bar + "\n")


if __name__ == "__main__":
    boot("Caesar Cipher", "CS-01", "classic shift cipher - encrypt / decrypt text")
