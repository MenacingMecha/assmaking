# elo-calc

Python script for calculating ELO and other player stats from a csv detailing all matches that took place.

## Getting Started

```
usage: elo-calc.py [-h] [-v] [-s] [-o OUTPUT_FILE] [-w WHITELIST_FILE]
                   [--print-output]
                   input_file

positional arguments:
  input_file         Input CSV containing details of matches

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  -s, --silent       Silences terminal output
  -o OUTPUT_FILE     Output CSV to write stats to
  -w WHITELIST_FILE  Newline-seperated list of players to check optionally
                     check against
  --print-output     Print stats to terminal (output is ugly, use for
                     debugging!)
```
