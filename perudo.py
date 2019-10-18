#!/usr/bin/env python3

import math
import sys
import matplotlib.pyplot as plot

NUM_DICE_SIDES = 6
MAX_NUM_DICE = 30

USAGE = '''
Usage:
./perudo.py num_dice_left my_dice out_file.csv

    num_dice_left       Count of the total number of dice remaining
    my_dice             Comma separated list of the dice in my hand (e.g. 1,4,4,5,6)
    out_file.csv        Destination for the output file

'''

def multinomial_coefficient (m, n):
    return math.factorial (m + n) // math.factorial (m) // math.factorial (n)

def n_choose_k (n, k):
    return math.factorial (n) // math.factorial (k) // math.factorial (n - k)

def n_multichoose_k (n, k):
    return multinomial_coefficient (n - 1, k)

class PerudoGame:

    def __init__ (self, num_dice, my_dice):
        self.num_dice       = num_dice
        self.my_dice        = my_dice
        self.probabilities  = []

        remaining_dice = num_dice - len (my_dice)

        # Given the set {1, 2, 3, ..., NUM_DICE_SIDES}, how many sets of size remaining_dice can be created? (repetition allowed)
        total_combinations = n_multichoose_k (NUM_DICE_SIDES, remaining_dice)
        print ('There are {} combinations'.format (total_combinations))

        self.count_probabilities = []

        for count in range (remaining_dice + 1):
            p = 1 / NUM_DICE_SIDES
            count_probability = n_choose_k (remaining_dice, count) * p ** count * (1 - p) ** (remaining_dice - count)
            self.count_probabilities.append (count_probability)

        for dice_value in range (1, NUM_DICE_SIDES + 1):

            probabilities = []

            my_count = my_dice.count (dice_value)

            for count in range (num_dice + 1):

                probability = 0

                if count <= my_count:
                    probability = 1.0
                elif count > my_count and count <= (my_count + remaining_dice):
                    start_index = count - my_count
                    probability = sum (self.count_probabilities [start_index:])

                probabilities.append (probability)

            self.probabilities.append (probabilities)
                
        assert len (self.probabilities) == NUM_DICE_SIDES
    

    def print_header (self, out_file):
        line = ' ,'

        for count in range (self.num_dice + 1):
            line += '{},'.format (count)

        out_file.write (line)
        out_file.write ('\n')


    def print_probabilities (self, out_file_path):

        out_file = open (out_file_path, 'w+')

        self.print_header (out_file)

        dice_value = 1

        for probabilities in self.probabilities:
            line = '{},'.format (dice_value)
            
            for count in range (self.num_dice + 1):
                line += '{},'.format (probabilities[count] * 100)

            dice_value += 1

            out_file.write (line)
            out_file.write ('\n')

        out_file.close ()

    def plot_graph (self):
        x = range (0, self.num_dice + 1)

        for dice_value in range (1, NUM_DICE_SIDES + 1):
            y_values = self.probabilities [dice_value - 1]
            label = '{}'.format (dice_value)
            assert (len (x) == len (y_values))
            plot.plot (x, y_values, label=label)


        plot.title ('Perudo Probabilities')
        plot.xlabel ('Num. rolls')
        plot.ylabel ('Probability')
        plot.legend ()
        plot.show ()



def get_num_dice (input_val):
    num_dice = int (input_val)

    if num_dice < 2 or num_dice > MAX_NUM_DICE:
        print ('Number of dice must be between 2 and {}'.format (MAX_NUM_DICE))
        sys.exit (1)

    return num_dice


def get_my_dice (input_val, num_dice):
    input_vals = input_val.split (',')

    my_dice = []
    for dice in input_vals:
        value = int (dice.strip ())

        if value < 1 or value > NUM_DICE_SIDES:
            print ('Dice value must be between 1 and {}'.format (NUM_DICE_SIDES))
            sys.exit (1)

        my_dice.append (value)

    if len (my_dice) >= num_dice:
        print ('Too many dice values specified')
        sys.exit (1)

    return my_dice


def main ():

    if len (sys.argv) != 4:
        print (USAGE)
        sys.exit (1)

    num_dice = get_num_dice (sys.argv [1])
    print ('There are {} dice left'.format (num_dice))

    my_dice = get_my_dice (sys.argv [2], num_dice)
    print ('I have {}'.format (my_dice))

    out_file = sys.argv [3]

    game = PerudoGame (num_dice, my_dice)
    game.print_probabilities (out_file)
    game.plot_graph ()

if __name__ == '__main__':
    main()