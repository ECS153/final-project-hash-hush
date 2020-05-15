import sys
from base_structure import extract_base

class Preterminal_Stats:
    """Record the Stats for the probabilities of base structs and digits and symbols"""

    def __init__(self):
        """Initialize the dictionaries that store the stats of the training wordlist"""
        # stats of bases
        # data structure: {<base>: <counter>}
        self.bases = {}
        # stats of digit streams, indexed by length n 
        # data structure: {<len>: {<digit stream>: <counter} }
        self.digits = {}
        # stats of symbol streams, indexed by length n
        # data structure: {<len>: {<symbol stream: <counter>} }
        self.symbols = {}

    def pw_stats(self, line):
        """generate the relevant stats about the input password"""
        statsOfPw = extract_base(line)
        if statsOfPw == None:
            return 
        # populate the bases
        base = statsOfPw["base"]
        if base in self.bases:
            self.bases[base] += 1
        else:
            self.bases[base] = 1
        
        # populate the digit streams
        digits = statsOfPw["digits"]
        for digitStream in digits.keys():
            streamLen = len(digitStream)
            counter = digits[digitStream] # number of occurences of that digit stream in that password
            if streamLen in self.digits: # digits table has stats of digit stream of length streamLen
                if digitStream in self.digits[streamLen]:
                    self.digits[streamLen][digitStream] += counter
                else:
                    self.digits[streamLen][digitStream] = counter
            else: 
                self.digits[streamLen] = {}
                self.digits[streamLen][digitStream] = counter
        
        # populate the symbol streams 
        symbols = statsOfPw["symbols"]
        for symbolStream in symbols.keys():
            streamLen = len(symbolStream)
            counter = symbols[symbolStream]
            if streamLen in self.symbols: # digits table has stats of digit stream of length streamLen
                if symbolStream in self.symbols[streamLen]:
                    self.symbols[streamLen][symbolStream] += counter
                else:
                    self.symbols[streamLen][symbolStream] = counter
            else: 
                self.symbols[streamLen] = {}
                self.symbols[streamLen][symbolStream] = counter
    
    def showBases(self):
        print (self.bases)
    
    def showDigits(self):
        print (self.digits)

    def showSymbols(self):
        print (self.symbols)

def main():
    # requires python 3 or above
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x", file=sys.stderr)
        sys.exit(1)

    # read in the name of the input file 
    try:
        fileName = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_wordlist>")

    # process each line in the input wordlist
    try:
        preterminal_stats = Preterminal_Stats()
        with open(fileName) as wordList:
            for line in wordList:
                preterminal_stats.pw_stats(line)
    except FileNotFoundError:
        print (f"Sorry, the file {fileName} does not exist")
    
    preterminal_stats.showBases()
    preterminal_stats.showDigits()
    preterminal_stats.showSymbols()
    
if __name__ == "__main__":
    main()