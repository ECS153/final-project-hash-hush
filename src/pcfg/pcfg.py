# Basic Usage: python pcfg.py <wordlist> <dict>
# Options: 
# <Tranining Mode>: -m <num>
#       1: terminal probability order (default)
#       2: pre-terminal probability order
# <Guessing Budget>: -b <num>
#       by default: 10 ^ 9


import sys
import argparse
from guess import Guess
from train import Train

def PCFGtrain(ts, dictionary, mode):
    """Train the pcfg model"""
    model = Train()

    # pw stats
    try:
        with open(ts, encoding='utf-8', errors='ignore') as wordList:
            for line in wordList:
                model.pw_stats(line)
    except FileNotFoundError:
        print (f"Sorry, the file {ts} does not exist")
    
    # dict stats
    if (dictionary):
        try:
            with open(dictionary, encoding='utf-8', errors='ignore') as         dictIonary:
                for line in dictIonary:
                    model.dict_stats(line.rstrip('\n'))
        except FileNotFoundError:
            print (f"Sorry, the file {dictionary} does not exist")
    
    model.showBases()
    #train.showDigits()
   # train.showSymbols()
    model.showDict()


def main():

    # requires python 3 or above
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x", file=sys.stderr)
        sys.exit(1)

    # Parsing the arguments and options 
    parser = argparse.ArgumentParser(description="PCFG: Pretty Cool Fuzzy Guesser")
    parser.add_argument("trainingSet", help="Use this wordlist to train the PCFG model")
    parser.add_argument("Dictionary", help="Use this dictionary to train the PCFG model and generate guesses")
    parser.add_argument("-m", "--mode", help="Specify the training mode, 1=terminal order, 2=preterminal order", type=int, choices=[1, 2], default=1)
    parser.add_argument("-b", "--budget", help="Specify the guessing budget", type=int)
    args = parser.parse_args()
    trainingSet = args.trainingSet
    dictionary = args.Dictionary
    mode = args.mode
    budget = args.budget

    # train the model
    model = PCFGtrain(trainingSet, dictionary, mode)
   
    
if __name__ == "__main__":
    main()