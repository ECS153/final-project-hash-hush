import sys, getopt
import numpy as np
import numpy
import itertools
import operator
import os

#-------------------------password guess generator-------------------------------

U = np.load("U.npy")
V = np.load("V.npy")
W = np.load("W.npy")
hidden_dim = 100
word_dim = 97

def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)

def generate_guess():
    pw = []
    s = np.zeros(hidden_dim)
    o = np.zeros(word_dim)
    char = 0
    prob = 1

    for t in np.arange(100):
        s = np.tanh(U[:, char] + W.dot(s))
        o = softmax(V.dot(s))
        
        char = np.random.choice(np.arange(0, 97), p=o)
        prob = 1 * o[char]
        
        if(char == 96 or char == 0):
            pw = [x + 31 for x in pw]
            s = ''.join(map(chr, pw))
            return s, prob
        pw.append(char)


#-------------------------command line parser------------------------------------
input = sys.argv[1:]
numGuesses = 0
outfile = ""
threshold = 0.25

try:
    opts, args = getopt.getopt(input,"o:n:p")
except getopt.GetoptError:
    print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")
    sys.exit(2)
    
for opt, arg in opts:
    if opt == "-o" :
        if ".txt" not in arg:
            print("Error: Output file must be a txt.")
            print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")
            sys.exit(2)
          
        outfile = arg
    elif opt == "-n":
        try:
            numGuesses = int(arg)
        except ValueError:
            print("Error: Number of Guesses must be integer")
            print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")
           
    elif opt == "-p":
        try:
            threshold = float(arg)
            if threshold > 1 or threshold < 0:
                print("Error: Probility must be a number between 0 and 1")
                print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")
        except ValueError:
            print("Error: Probility must be a number between 0 and 1")
            print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")

if(outfile == "" or numGuesses == 0):
    print("Error: Must have an output file and number of guesses to be generated")
    print("pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>")
    sys.exit(2)
    

#---------------------------------------------------------------------------
prefix = outfile.split(".")[0]
fcount = 0
file = open(prefix + "_" + str(fcount) + ".txt" , 'w')
i = 1

while i < numGuesses:
    s, prob = generate_guess()
    if(prob > threshold):
        i = i + 1
        file.writelines(s + '\n')
        if i % 35000000 == 0:
            fcount = fcount + 1
            file.close()
            print(str(i) + " passwords are generated")
            file = open(prefix + "_" + str(fcount) + ".txt" , 'w')
    

    

a = prefix + "_" + str(fcount) + ".txt"
if(os.stat(a).st_size == 0):
    os.remove(a)

