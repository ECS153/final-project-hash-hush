"""Train the PCFG model"""

import sys
import re
from preprocessing import extract_stats

class Train:
    """Record the Stats for the probabilities of base structs and digits and symbols"""

    def __init__(self):
        """Initialize the dictionaries that store the stats of the training wordlist"""
        # stats of bases
        # data structure: {<base>: <counter>}
        self.bases = {}
        # stats of digit streams, keyed by len 
        # data structure: {<len>: {<digit stream>: <counter>} }
        self.digits = {}
        # stats of symbol streams, keyed by len
        # data structure: {<len>: {<symbol stream: <counter>} }
        self.symbols = {}
        # partitions the dictionary by len 
        # data structure: {<len>: <words>}; <words> is a vector of string
        self.alphas = {}
        # size of the dictionary 
        self.dictSize = 0
        # size of the wordlist 
        self.listSize = 0


    def pw_stats(self, line):
        """generate the relevant stats about the input password"""
        self.listSize += 1

        statsOfPw = extract_stats(line)
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

    
    def base_organize(self, mode):
        """Organize the structure of the base (occurences -> probability), modify the probability based on the mode"""

        for base in self.bases:
            self.bases[base] /= self.listSize

        if (mode == 1): # terminal order 
            # Modify the base probability based on the dictionary:
            # The probability of L3, for example is the number of 3 letter words in the dictionary divided by the size of the dictionary
            wordProb = {}
            for leng in self.alphas:
                wordProb['L'+ str(leng)] = len(self.alphas[leng]) / self.dictSize

            pattern = re.compile('L[0-9]+')
            for base in self.bases:
                matches = pattern.findall(base)
                if matches: # if match
                    for match in matches:
                        if match in wordProb:
                            self.bases[base] *= wordProb[match]
                        else:
                            self.bases[base] = 0


    def ds_organize(self):
        """Organize the structure of the Digits and Symbols (occurences -> probability) and sort them by probability; prob table for each length"""
        # digits
        for len, digits in self.digits.items():
            # for a given length, sum the number of occurrences 
            allOccurences = sum(digits.values())
            # occurences ==> probability 
            for sequence in digits:
                digits[sequence] /= allOccurences 
            # sort the sequences, given the len, by probability
            # Data structure of self.digits:
            # {<len>: [(<seq>, <prob>)]}, <seq> is the digit sequence string, <prob>: the probability of that sequence given the length
            self.digits[len] = sorted(digits.items(), key=lambda x: x[1], reverse=True)
        
        # symbols
        for len, symbols in self.symbols.items():
            # for a given length, sum the number of occurrences 
            allOccurences = sum(symbols.values())
            # occurences ==> probability 
            for sequence in symbols:
                symbols[sequence] /= allOccurences 
            # sort the sequences, given the len, by probability
            # Data structure of self.symbols:
            # {<len>: [(<seq>, <prob>)]}, <seq> is the symbol sequence string, <prob>: the probability of that sequence given the length
            self.symbols[len] = sorted(symbols.items(), key=lambda x: x[1], reverse=True)

  
    def dict_stats(self, line):
        """partitions the dictionary by len"""

        ## Assume the input dict file is one word per line, delimited by the new line char. The last line of the file is a newline char

        self.dictSize += 1

        wordLen = len(line) 
        if wordLen not in self.alphas:
            self.alphas[wordLen] = []
    
        self.alphas[wordLen].append(line)

    
    def printBases(self):
        """Stats of bases, in decreasing order"""
        print ("{:<12} {:<15}".format('Base','Probability'))
        for base in self.bases:
            print ("{:<12} {:<15}".format(base, self.bases[base]))


    def printDigits(self):
        """Stats of digit streams, in decreasing order"""

        for len, digits in self.digits.items():
            print (f"Stats for digit streams of length {len}: ")
            print ("{:<8} {:<15}".format('Digits','Probability'))
            for sequence in digits:
                print ("{:<8} {:<15}".format(sequence[0], '%.3f'%(sequence[1])))


    def printSymbols(self):
        """Stats of symbol streams, in decreasing order"""

        for len, symbols in self.symbols.items():
            print (f"Stats for symbol streams of length {len}: ")
            print ("{:<8} {:<15}".format('Symbols','Probability'))
            for sequence in symbols:
                print ("{:<8} {:<15}".format(sequence[0], '%.3f'%(sequence[1])))


    def printDict(self):
        """Stats of the dictionary"""
        print (f"The size of the input dictionary is {self.dictSize}")
        

    def printList(self):
        """Stats of the wordlist"""
        print (f"The size of the input wordlist is {self.listSize}")
        


def main():

    print ("Please refer to README for usage and examples")
     # read in the name of the wordlist 
    try:
        wordlist = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <wordlist> <dictionary>")

    # process each line in the input wordlist
    try:
        train = Train()
        with open(wordlist, encoding='utf-8', errors='ignore') as wordList:
            for line in wordList:
                train.pw_stats(line)
    except FileNotFoundError:
        print (f"The file {wordlist} does not exist")

    # read in the name of the dictionary  
    try:
        dictionary = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <wordlist> <dictionary>")

    # process each line in the input dictionary 
    try:
        with open(dictionary, encoding='utf-8', errors='ignore') as dictIonary:
            for line in dictIonary:
                train.dict_stats(line.rstrip('\n'))
    except FileNotFoundError:
        print (f"The file {dictionary} does not exist")
    
    train.printDigits()
    

if __name__ == "__main__":
    main()