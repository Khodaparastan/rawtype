# rawtype

A macOS keyboard typing automation tool that simulates hardware keystrokes using AppleScript keycodes. Useful for typing into environments where standard clipboard paste doesn't work, such as VNC sessions and virtual machines.

## Requirements

- macOS
- Python 3.13+
- [Poetry](https://python-poetry.org/) for dependency management

## Installation
```
bash
poetry install
```
## Usage

### Type a string directly
```
bash
rawtype text "Hello, World!"
```
### Type the contents of a file
```
bash
rawtype file path/to/file.txt
```
### Type from stdin
```
bash
echo "Hello, World!" | rawtype stdin
cat file.txt | rawtype stdin
```
### Run a keyboard mapping test
```
bash
rawtype test
```
## Options

| Option               | Default | Description                                        |
|----------------------|---------|----------------------------------------------------|
| `-d`, `--delay`      | `0.05`  | Delay between keystrokes in seconds                |
| `-w`, `--wait`       | `3`     | Countdown in seconds before typing starts          |
| `-v`, `--verbose`    | `false` | Show detailed output, including skipped characters |
| `-c`, `--chunk-size` | `100`   | *(file only)* Characters per chunk                 |

## Notes

- Characters not found in the ANSI (US) keymap are silently skipped; use `--verbose` to see which ones.
- The `file` command processes content in chunks to avoid AppleScript memory limits.
- Make sure the target window is focused before the countdown ends.