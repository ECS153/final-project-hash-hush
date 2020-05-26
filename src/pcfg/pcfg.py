# Basic Usage: python pcfg.py <wordlist> <dict>
# Options: 
# <Tranining Mode>: -m <num>
#       1: terminal probability order (default)
#       2: pre-terminal probability order
# <Guessing Budget>: -b <num>
#       by default: 10 ^ 4


import sys
import argparse
from guess import GuessGen
from train import Train

def pcfgTrain(ts, dictionary, mode):
    """Train the pcfg model"""
    model = Train()

    # pw stats
    try:
        with open(ts, encoding='utf-8', errors='ignore') as wordList:
            for line in wordList:
                model.pw_stats(line)
    except FileNotFoundError:
        print (f"The file {ts} does not exist")
    
    # dict stats
    try:
        with open(dictionary, encoding='utf-8', errors='ignore') as         dictIonary:
            for line in dictIonary:
                model.dict_stats(line.rstrip('\n'))
    except FileNotFoundError:
        print (f"The file {dictionary} does not exist")

    # process the training output to the desired format 
    model.base_organize(mode)
    model.ds_organize()

    return model


def pcfgGuess(budget, model):
    """Generate guesses based on the trained model and guessing budget"""

    guesser = GuessGen(model)
    # step 1: generate pre-terminal structures 
    # 1.1: initialize the priority queue with the highest prob pre-terminal structure instance of all base strucures 
    guesser.pqInit()
    guesser.printPq()
   
    # while the guesser can still generate guesses 
    # while (not guesser.finished): # and guesser.guessingNumber <= budget):
    #     # 1.2: implement the `next` function that inserts pre-terminal strucutures into the queue when one pre-terminal struct is popped from the queue
    #     preterminal = guesser.pqPopInsert()
    #     # step 2: generate actual guesses
    #     # feed the preterminal to the guesser to fill the 'L#' structures 
    #     guesses = guesser.guess(preterminal, budget)


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
    parser.add_argument("-b", "--budget", help="Specify the guessing budget", type=int, default=10000)
    args = parser.parse_args()

    # train the model
    model = pcfgTrain(args.trainingSet, args.Dictionary, args.mode)

    # generate guesses
    pcfgGuess(args.budget, model)
    
   
    
if __name__ == "__main__":
    main()