# Purpose: parse the base structure of an input password 
# input: a password in the training wordlist 
# output: the base structure of the password
# available variables (nonterminals):
# Ln, Sn, Dn
# Ln: alpha string of length n (contains only English alphabet)
# Sn: special symbol  string of length n (contains only special symbols)
# Dn: digit strings of length n (contains only digits)

# Note: Special symbol is defined as non-digit and non-alphabet
# TODO: add custom dictionary (terminals)

import sys

def extract_base(line, charSet={}):
    
    l = s = d = 0
    base = ""
    digitStream = ""
    symbolStream = ""
    # record the stats of the pw
    statsOfPw = {}

    # invariant: At any moment, no more than one of the l, s, d will be nonzero
    # When in the process of parsing a non-empty line, exactly one of the l, s, d will be nonzero. 
    for c in line: 
        if c.isalpha():
            if s != 0: # the specical symbol stream has ended              
                base += f"S{s}"                
                # save the symbol stream and the counter of the stream 
                if symbolStream in statsOfPw: 
                    statsOfPw[symbolStream] += 1
                else:
                    statsOfPw[symbolStream] = 1
                # flush the temp variable to keep the invariant
                s = 0 
                symbolStream = ""
            elif d != 0: # the number stream has ended 
                base += f"D{d}"  
                # save the digit stream and the counter of the stream             
                if digitStream in statsOfPw: 
                    statsOfPw[digitStream] += 1
                else:
                    statsOfPw[digitStream] = 1
                # flush the temp variable
                d = 0
                digitStream = ""
            l += 1

        elif c.isdigit():
            if l != 0: # the letter stream has ended              
                base += f"L{l}"
                l = 0
            elif s != 0: # the specical symbol stream has ended 
                base += f"S{s}"
                if symbolStream in statsOfPw: 
                    statsOfPw[symbolStream] += 1
                else:
                    statsOfPw[symbolStream] = 1
                s = 0
                symbolStream  = ""
            d += 1
            digitStream += c

        elif c == '\n':
            if l != 0: # the letter stream has ended              
                base += f"L{l}"
                l = 0
            elif s != 0: # the specical symbol stream has ended 
                base += f"S{s}"            
                if symbolStream in statsOfPw: 
                    statsOfPw[symbolStream] += 1
                else:
                    statsOfPw[symbolStream] = 1
                s = 0
                symbolStream  = ""
            elif d != 0:
                base += f"D{d}"
                if digitStream in statsOfPw: 
                    statsOfPw[digitStream] += 1
                else:
                    statsOfPw[digitStream] = 1
                d = 0
                digitStream = ""
            else: # this line only contains the new line char
                return 

        else: # encounters special symbol 
            if l != 0: # the letter stream has ended              
                base += f"L{l}"
                l = 0
            elif d != 0: # the number stream has ended 
                base += f"D{d}"
                if digitStream in statsOfPw: 
                    statsOfPw[digitStream] += 1
                else:
                    statsOfPw[digitStream] = 1
                d = 0
                digitStream = ""
            s += 1
            symbolStream += c
    
    statsOfPw["base"] = base
    return statsOfPw

def main():
    """For testing purpose"""
    try:
        fileName = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input_wordlist>")

    # process each line in the input wordlist
    try:
        with open(fileName) as wordList:
            for line in wordList:
                stats = extract_base(line)
                print (stats)
    except FileNotFoundError:
        print (f"Sorry, the file {fileName} does not exist")    
    
if __name__ == "__main__":
    main()


    




