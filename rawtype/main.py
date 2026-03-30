#!/usr/bin/env python3
"""
rawtype - Keyboard typing automation for macOS
Simulates keyboard input using hardware keycodes
"""

import subprocess
import sys
import time
from pathlib import Path

import click

# Mac hardware keycodes for ANSI(US) layout
KEYMAP = {
    # Letters
    "a": 0,
    "b": 11,
    "c": 8,
    "d": 2,
    "e": 14,
    "f": 3,
    "g": 5,
    "h": 4,
    "i": 34,
    "j": 38,
    "k": 40,
    "l": 37,
    "m": 46,
    "n": 45,
    "o": 31,
    "p": 35,
    "q": 12,
    "r": 15,
    "s": 1,
    "t": 17,
    "u": 32,
    "v": 9,
    "w": 13,
    "x": 7,
    "y": 16,
    "z": 6,
    # Numbers
    "0": 29,
    "1": 18,
    "2": 19,
    "3": 20,
    "4": 21,
    "5": 23,
    "6": 22,
    "7": 26,
    "8": 28,
    "9": 25,
    # Special characters (unshifted)
    "`": 50,
    "-": 27,
    "=": 24,
    "[": 33,
    "]": 30,
    "\\": 42,
    ";": 41,
    "'": 39,
    ",": 43,
    ".": 47,
    "/": 44,
    " ": 49,  # Space
}

# Shifted characters mapping
SHIFT_MAP = {
    "~": "`",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "<": ",",
    ">": ".",
    "?": "/",
}


def type_string(in_text, delay=0.05, verbose=False):
    """Type a string using AppleScript key codes."""
    applescript = ['tell application "System Events"']
    skipped = []

    for i, char in enumerate(in_text):
        # Handle newline
        if char == "\n":
            applescript.append("key code 36")
            applescript.append(f"delay {delay * 6}")
            continue

        # Handle tab
        if char == "\t":
            applescript.append("key code 48")
            applescript.append(f"delay {delay}")
            continue

        # Check if character needs shift
        needs_shift = False
        base_char = char

        if char.isupper():
            needs_shift = True
            base_char = char.lower()
        elif char in SHIFT_MAP:
            needs_shift = True
            base_char = SHIFT_MAP[char]

        # Get keycode
        if base_char in KEYMAP:
            code = KEYMAP[base_char]
            if needs_shift:
                applescript.append(f"key code {code} using shift down")
            else:
                applescript.append(f"key code {code}")
            applescript.append(f"delay {delay}")
        else:
            skipped.append((i, char, ord(char)))

    applescript.append("end tell")

    script = "\n".join(applescript)

    try:
        subprocess.run(
            ["osascript", "-e", script], check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"AppleScript error: {e.stderr}")

    if skipped and verbose:
        click.echo(click.style("\nSkipped characters:", fg="yellow"), err=True)
        for pos, char, code in skipped:
            click.echo(f"  Position {pos}: '{char}' (U+{code:04X})", err=True)

    return len(skipped)


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0")
def cli(ctx):
    """
    rawtype - Keyboard typing automation for macOS

    Simulates keyboard input using hardware keycodes for reliable typing
    across applications, including VNC sessions and virtual machines.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("in_text")
@click.option(
    "-d",
    "--delay",
    default=0.05,
    type=float,
    help="Delay between keystrokes in seconds (default: 0.05)",
)
@click.option(
    "-w",
    "--wait",
    default=3,
    type=int,
    help="Countdown before typing starts (default: 3)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show detailed output including skipped characters",
)
def text(in_text, delay, wait, verbose):
    """Type a in_text string."""
    if wait > 0:
        with click.progressbar(
            range(wait),
            label="Starting in",
            bar_template="%(label)s %(info)s seconds",
            show_eta=False,
            show_percent=False,
        ) as bar:
            for _ in bar:
                time.sleep(1)

    if verbose:
        click.echo(f"Typing {len(in_text)} characters...", err=True)

    skipped = type_string(in_text, delay, verbose)

    if verbose:
        click.secho(
            f"✓ Complete ({len(in_text) - skipped}/{len(in_text)} characters typed)",
            fg="green",
            err=True,
        )


@cli.command()
@click.argument("in_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-d",
    "--delay",
    default=0.05,
    type=float,
    help="Delay between keystrokes in seconds (default: 0.05)",
)
@click.option(
    "-w",
    "--wait",
    default=3,
    type=int,
    help="Countdown before typing starts (default: 3)",
)
@click.option(
    "-c",
    "--chunk-size",
    default=100,
    type=int,
    help="Characters per chunk to avoid memory limits (default: 100)",
)
@click.option("-v", "--verbose", is_flag=True, help="Show detailed progress")
def file(in_file, delay, wait, chunk_size, verbose):
    """Type contents of a in_file."""
    path = Path(in_file)

    try:
        content = path.read_text()
    except Exception as e:
        raise click.ClickException(f"Failed to read in_file: {e}")

    if wait > 0:
        with click.progressbar(
            range(wait),
            label="Starting in",
            bar_template="%(label)s %(info)s seconds",
            show_eta=False,
            show_percent=False,
        ) as bar:
            for _ in bar:
                time.sleep(1)

    total_chars = len(content)
    chunks = [content[i : i + chunk_size] for i in range(0, total_chars, chunk_size)]

    if verbose:
        click.echo(
            f"Typing {total_chars} characters in {len(chunks)} chunks...", err=True
        )

    total_skipped = 0

    with click.progressbar(
        chunks, label="Progress", show_eta=True if len(chunks) > 10 else False
    ) as bar:
        for chunk in bar:
            skipped = type_string(chunk, delay, False)
            total_skipped += skipped
            time.sleep(0.1)  # Pause between chunks

    if verbose:
        click.secho(
            f"✓ Complete ({total_chars - total_skipped}/{total_chars} characters typed)",
            fg="green",
            err=True,
        )


@cli.command()
@click.option(
    "-w",
    "--wait",
    default=3,
    type=int,
    help="Countdown before typing starts (default: 3)",
)
@click.option(
    "-d",
    "--delay",
    default=0.05,
    type=float,
    help="Delay between keystrokes in seconds (default: 0.05)",
)
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
def stdin(wait, delay, verbose):
    """Type in_text from stdin (pipe or redirect)."""
    if sys.stdin.isatty():
        raise click.ClickException("No input provided. Use: echo 'in_text' | rawtype stdin")

    content = sys.stdin.read()

    if not content:
        raise click.ClickException("Empty input")

    if wait > 0:
        with click.progressbar(
            range(wait),
            label="Starting in",
            bar_template="%(label)s %(info)s seconds",
            show_eta=False,
            show_percent=False,
        ) as bar:
            for _ in bar:
                time.sleep(1)

    if verbose:
        click.echo(f"Typing {len(content)} characters...", err=True)

    skipped = type_string(content, delay, verbose)

    if verbose:
        click.secho(
            f"✓ Complete ({len(content) - skipped}/{len(content)} characters typed)",
            fg="green",
            err=True,
        )


@cli.command()
def test():
    """Run a test to verify keyboard mapping."""
    test_text = """abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789
!@#$%^&*()_+-=[]{}\\|;:'",.<>?/~`
Tab\ttest\there
Multiple
lines
work"""

    click.echo("Test in_text:")
    click.echo(click.style(test_text, fg="cyan"))
    click.echo()

    if not click.confirm("Ready to type this in 3 seconds?"):
        return

    with click.progressbar(
        range(3),
        label="Starting in",
        bar_template="%(label)s %(info)s seconds",
        show_eta=False,
        show_percent=False,
    ) as bar:
        for _ in bar:
            time.sleep(1)

    type_string(test_text, delay=0.05, verbose=True)
    click.secho("✓ Test complete", fg="green")


if __name__ == "__main__":
    cli()
