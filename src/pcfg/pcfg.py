# Basic Usage: python pcfg.py 
# Options: 
# <Training Data>: -d <wordlist> <dict>
#       
# <Tranining Mode>: -m <num>
#       1: terminal probability order (default)
#       2: pre-terminal probability order
# <Guessing Budget>: -b <num>
#       by default: 10 ^ 4
# <Save Training>: -s <file>
#   - save the training result to a file 
# <Load Traning>: -l <file>
#   - load the training result from a file and generate guesses based on the loaded model
#   - mutually exclusive with '-d'
#   - mutually exclusive with '-s'


import sys
import argparse
import pickle
from guess import GuessGen
from train import Train

def pcfgTrain(ts, dictionary, mode, save):
    """Train the pcfg model"""
    model = Train()

    # pw stats
    try:
        with open(ts, encoding='utf-8', errors='ignore') as wordList:
            for line in wordList:
                model.pw_stats(line)
    except FileNotFoundError:
        print (f"The file {ts} does not exist", file=sys.stderr)
    
    # dict stats
    try:
        with open(dictionary, encoding='utf-8', errors='ignore') as         dictIonary:
            for line in dictIonary:
                model.dict_stats(line.rstrip('\n'))
    except FileNotFoundError:
        print (f"The file {dictionary} does not exist", file=sys.stderr)

    # process the training output to the desired format 
    model.base_organize(mode)
    model.ds_organize()

    # save the trained model 
    if save: 
        # write to the file
        try:
            with open(save, 'wb') as s:
               pickle.dump(model, s)
        except FileNotFoundError:
            print (f"The file {s} is not writeable", file=sys.stderr)

        print(f"The model is written into the {save}")
        sys.exit(0)

    return model


def pcfgGuess(budget, model):
    """Generate guesses based on the trained model and guessing budget"""

    guesser = GuessGen(model)
    # step 1: generate pre-terminal structures 
    # 1.1: initialize the priority queue with the highest prob pre-terminal structure instance of all base strucures 
    guesser.pqInit()

    # while the guesser can still generate guesses 
    # 2 cases when finished
    # 1): the guesser generates all possible guesses
    # 2): exceed the budget 
    # 3): TODO: when user presses ctrl-c
    while (guesser.guessingNumber < budget):

        # 1.2: implement the `next` function that inserts pre-terminal strucutures into the queue when one pre-terminal struct is popped from the queue
        preterminal = guesser.pqPopInsert()
        # step 2: generate actual guesses
        # feed the preterminal to the guesser to fill the 'L#' structures 
        guesser.guess(preterminal)


def main():

    # requires python 3 or above
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x", file=sys.stderr)
        sys.exit(1)

    # Parsing the arguments and options 
    parser = argparse.ArgumentParser(description="PCFG: Pretty Cool Fuzzy Guesser")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--data",nargs="+", help="Use the input wordlist and dictionary to train the PCFG model")
    group.add_argument("-l", "--load", help="Load the trained model from a file", type=str)
    parser.add_argument("-m", "--mode", help="Specify the training mode, 1=terminal order, 2=preterminal order", type=int, choices=[1, 2], default=1)
    parser.add_argument("-b", "--budget", help="Specify the guessing budget", type=int, default=10000)
    parser.add_argument("-s", "--save", help="Train the model and save the trained model to a file", type=str)

    args = parser.parse_args()

    # -l and -s are mutually exclusive
    if args.save and args.load:
        print ("-s/--save and -l/--load are mutually exclusive", file=sys.stderr)
        sys.exit(1)

    # load the trained model
    if args.load:
        try:
            with open(args.load, 'rb') as m:
                model = pickle.load(m)
        except FileNotFoundError:
            print (f"The file {args.load} does not exist", file=sys.stderr)

    else:
        # training data should contain two files: training wordlist and dictionary
        if len(args.data) != 2:
            print ("-d/--data should be followed by two files", file=sys.stderr)
            sys.exit(1)
        # train the model
        model = pcfgTrain(args.data[0], args.data[1], args.mode, args.save)

    # generate guesses
    pcfgGuess(args.budget, model)



if __name__ == "__main__":
    main()