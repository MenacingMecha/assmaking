from trueskill import *
import csv
import sys
import argparse

class InputCSV:
    def __init__(self, pathtofile):
        '''
        Parameters
        ----------
        pathtofile : string
            The path to the input file
        '''
        self.inputFile = open(pathtofile)
        self.read = csv.reader(self.inputFile, delimiter=',')

    def get_names(self):
        ''' Get all player's names, sorted by rank position '''
        players = []
        self.reset_csv()
        for r in self.read:
            players.append([r[0], r[1]])  # 1st index is position, 2nd is name
        sorted(players, key=lambda player: player[0])  # sort by position
        return players

    def reset_csv(self):
        ''' Resets the file seek on the input CSV back to the start of data, skipping the header '''
        self.inputFile.seek(0)
        next(self.read)

    def close_data(self):
        ''' Closes the opened input CSV '''
        self.inputFile.close()

def get_players_present(pathtofile):
    '''
    Returns an array of players from the supplied, line seperated register file

    Parameters
    ----------
    pathtofile : string
        The path to the input file

    Returns
    -------
    players_present : list
        Array of every player present
    '''
    players_present = []
    with open(pathtofile, "r") as registerFile:
        for line in registerFile:
            name = line.rstrip()
            players_present.append(name)
    return players_present

def argParse():
    '''Returns a list of parsed command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('playerdata_file', action='store',
            help='Input CSV containing information on all players')
    parser.add_argument('register_file', action='store',
            help='Line-seperated list of present players')
    parser.add_argument('-s', '--silent', action='store_true', default=False,
            dest="silent", help='Silences terminal output')
    parser.add_argument('-o', action='store', dest='output_file',
            help='Output CSV to write matches to')
    parser.add_argument('--print-output', action='store_true', default=False,
            dest='print_output',
            help='Print stats to terminal (output is ugly, use for debugging!)')
    return parser.parse_args()

def get_players_to_match(present_players, all_players):
    ''' Loops through all players (sorted by rank), returning an array of every present player '''
    players_to_match = []
    for ap in all_players:
        for pp in present_players:
            if pp == ap[1]:  # check if names are equal
                players_to_match.append(ap)
                present_players.remove(pp)
                break  # player has been found, break loop early
    #players_to_match.reverse()  # does this need to be reversed or not?
    return players_to_match

def generate_matches(players_to_match):
    matches = []
    total_players = len(players_to_match)
    odd_number_of_players = total_players % 2 != 0
    while len(players_to_match) > 0:
        print(len(players_to_match))
        # if there's an odd number of players, the first player is given another match
        second_run = len(players_to_match) == total_players - 2
        print(second_run)
        if second_run and odd_number_of_players:
            print("LETS GOOO")
            player_a = matches[0][0]
        else:
            # take the player at the bottom of the list
            player_a = players_to_match[-1]
            players_to_match.remove(player_a)
        player_b = players_to_match[-1]  # TODO: change this to match randomly
        players_to_match.remove(player_b)
        match = [player_a, player_b]
        print(match)
        matches.append(match)
    return matches

def main():
    global ARGS
    ARGS = argParse()
    player_data_file = InputCSV(ARGS.playerdata_file) # TODO: rename this method call
    players_total = player_data_file.get_names()
    player_data_file.close_data()
    players_present = get_players_present(ARGS.register_file)
    players_to_match = get_players_to_match(players_present, players_total)
    for p in players_to_match:
        print(p)
    matches = generate_matches(players_to_match)
    print(len(matches))
    for p in matches:
        print(p)

if __name__ == "__main__":
    main()
