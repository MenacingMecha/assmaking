# elo-calc

Python script for calculating ELO and other player stats from a csv detailing all matches that took place.

## Getting Started

Record each match that takes place in a csv file, with a the first two columns containing the players (or teams) involved, and with the third column denoting which of these two won.

If your csv isn't laid out in this way (mine aren't), you can specify how many columns to offset with with the -x option.

By default, it parses through the input csv to populate the list of players, although you can specify a newline seperate whitelist of players with the -w option, with matches containing players not on the whitelist being ignored for stats purposes.

In order for players with very few matches to not have an unfair advantage in terms of tournament seeding, players with 5 or less games are considered in "placement" status, with their Elo rating set to equal the amount of games they have played.

## Usage

```
usage: elo-calc.py [-h] [-v] [-s] [-o OUTPUT_FILE] [-w WHITELIST_FILE]
                   [--print-output] [-x OFFSET]
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
  -x OFFSET          How many columns to offset in the input CSV
```

## Example

```
$ cat input.csv

no.,date,challenger,defendant,winner,notes
1,2018-03-29,playerA,playerB,playerA,
2,2018-03-30,playerA,playerC,playerA,
3,2018-03-30,playerB,playerC,playerB,
4,2018-03-30,playerB,playerC,playerC,bracket reset
5,2018-03-31,playerA,playerC,playerC,
6,2018-03-31,playerA,playerB,playerA,
7,2018-03-31,playerA,playerC,playerA,
8,2018-03-31,playerB,playerC,playerB,
9,2018-03-31,playerB,playerC,playerC,
10,2018-03-31,playerA,playerD,playerD,playerD's debut

$ python elo-calc.py -s -x 2 -o output.csv input.csv

$ cat output.csv

Player,Elo,Games,Wins,Losses,Winrate,Highest Elo,Lowest Elo
playerB,1169.2631540771322,6,2,4,0.3333333333333333,1200.0082819270542,1169.2631540771322
playerC,1192.5416461806617,7,3,4,0.42857142857142855,1201.6756046670093,1171.4550509140513
playerA,1206.2460183474323,6,4,2,0.6666666666666666,1227.845511608049,1200
playerD,1,1,1,0,1.0,1,1
```
