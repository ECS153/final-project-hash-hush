"""An effective guess generation algo that generates guesses based on the training result"""

from queue import PriorityQueue
import re
import sys
import copy

Lp = re.compile('L')
Dp = re.compile('D')
Sp = re.compile('S')


def parseBase(base):
    """Takes in a base string and parse it to a list of substrings (subbases)"""
    # eg: "L3D12S1" ==> ["L3", "D12", "S1"]

    baseList = []

    for sB in re.finditer(r'[LDS]\d+', base):
        baseList.append(base[sB.start(): sB.end()])

    return baseList

def extractIndex(base, pv):
    """find the index to be changed in the parent preterminal string"""
    # index[0]: the length of previous chars: the starting position in the preterminal
    # index[1]: the length of the token to be replaced 
    index = [0] * 3
    prev = "".join(base[0: pv])
    index[0] = sum(map(int, re.findall(r'\d+', prev)))
    index[1] = int(re.search(r'\d+', base[pv]).group())

    return index


# tResult: the result of training
# finished: flag to indicate if the guesser has finished guessing 
#       1: deplete the guessing budget 
#       2: has tried all guesses
# guessingNumber: keep track of how many guesses has been generated
# pq: the priority queue that holds the pre-terminal structs
# budget: guessing budget

class GuessGen:
    """Generate guesses"""
    def __init__(self, tResult, budget):
        self.tResult = tResult
        self.finished = False
        self.guessingNumber = 0
        self.pq = PriorityQueue()
        self.budget = budget


    def pqInit(self):
        """Initialize the priority Queue"""
        # A queue object:
        # [<prob>, <base>, <pv>, <preterminal>, <tableIndices>]
        # <prob>: a floating number, the actual prob * -1
        # <base>: list of sub-bases; each subbases is a string 
        # <pv>: a non-nagative int
        # <preterminal>: list of chars
        # <tableIndices>: list of indices 
        
        for base in self.tResult.bases:
            qObject = [None] * 5
            qObject[1] = parseBase(base)
            qObject[2] = 0
            prob = -1 * self.tResult.bases[base]
            preterminal = ""
            
            for sB in qObject[1]:
                if Lp.match(sB): # if the sub-base contains letter 'L': an alpha sub-base
                    preterminal += sB
                    continue
                else: # an digit or symbol sub-base: substitute
                    leng = int(sB[1: ])
                    if Dp.match(sB): # a digit sub-base
                        # first []: goes to the table of "digit sequence of length `leng`"
                        # second[]: goes to the highest prob digit sequence of than leng
                        # third []: extract the digit string
                        preterminal += self.tResult.digits[leng][0][0]
                        prob *= self.tResult.digits[leng][0][1]

                    elif Sp.match(sB): # a symbol sub-base
                        preterminal += self.tResult.symbols[leng][0][0]
                        prob *= self.tResult.symbols[leng][0][1]

                    else:
                        print ("Error!")
                        sys.exit(1)

            qObject[3] = list(preterminal)
            qObject[4] = [0] * len(qObject[1])
            qObject[0] = prob
            # insert the q object into the pq
            self.pq.put(qObject)

    def printPq (self):

        queueCopy = PriorityQueue()

        row_format ="{:<}" + "{:>15}" * 4 + "{:>20}"
        print(row_format.format("",'Probability','Sub-Bases', 'Pivot Value', 'Pre-terminal','Indices'))

        while not self.pq.empty():
            qObject = self.pq.get()
            if qObject[0] == 0:
                print(row_format.format("", '0' , "".join(qObject[1]), qObject[2], qObject[3], str(qObject[4])))
            else:
                print(row_format.format("", '%.3f'%(-1 * qObject[0]), "".join(qObject[1]), qObject[2], "".join(qObject[3]), str(qObject[4])))

            queueCopy.put(qObject)
        
        self.pq = queueCopy
 

    def pqPopInsert(self):
        """Pop the highest probable pre-terminal struct from the queue and Insert its children"""
        qObject = self.pq.get()
        pv = qObject[2]
        base = qObject[1]

        for i, sB in enumerate(base):
            if i < pv or Lp.match(sB):
                continue 
        
            else:
                # check if there would be no child preterminal of this pv value: the replacement pool have been exhausted

                # go to the pool (eg: D2, S3)
                index = extractIndex(base, i)
                isdigit = Dp.match(sB)
                if isdigit and qObject[4][i] == self.tResult.digitStats[index[1]]:
                    continue
                # symbol table 
                elif not isdigit and qObject[4][i] == self.tResult.symbolStats[index[1]]:
                    continue
            
                newQObject = copy.deepcopy(qObject)
                # set the pv value 
                newQObject[2] = i
                # increment the position in the pool 
                newQObject[4][i] += 1
                # modify the probability 
                if isdigit:
                    original = self.tResult.digits[index[1]][qObject[4][i]]
                    new = self.tResult.digits[index[1]][newQObject[4][i]]
                else:
                    original = self.tResult.symbols[index[1]][qObject[4][i]]
                    new = self.tResult.symbols[index[1]][newQObject[4][i]]
                newQObject[0] = qObject[0] / original[1] * new[1]
                # modify the pre-terminal
                newQObject[3][index[0]: index[0]+index[1]] = list(new[0])
                # push the new queue object into the queue 
                self.pq.put(newQObject)
        
        return qObject[3]
    

    def guess(self, preterminal):
        """Generate the actual text guesses"""



    


def main():
    print ("Please refer to README for usage and examples")

   
if __name__ == "__main__":
    main()