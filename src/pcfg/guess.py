"""An effective guess generation algo that generates guesses based on the training result"""

from queue import PriorityQueue
import re
import sys


def parseBase(base):
    """Takes in a base string and parse it to a list of substrings (subbases)"""
    # eg: "L3D12S1" ==> ["L3", "D12", "S1"]

    baseList = []

    for sB in re.finditer(r'[LDS]\d+', base):
        baseList.append(base[sB.start(): sB.end()])

    return baseList


# tResult: the result of training
# finished: flag to indicate if the guesser has finished guessing 
#       1: deplete the guessing budget 
#       2: has tried all guesses
# guessingNumber: keep track of how many guesses has been generated
# pq: the priority queue that holds the pre-terminal structs

class GuessGen:
    """Generate guesses"""
    def __init__(self, tResult):
        self.tResult = tResult
        self.finished = False
        self.guessingNumber = 0
        self.pq = PriorityQueue()

   
    def pqInit(self):
        """Initialize the priority Queue"""
        # A queue object:
        # (<prob>, {'base': <base struct>, 'preterminal': <preterminal struct>, 'pv': pivot value}, 'tableIndices': [])
        Lp = re.compile('L')
        Dp = re.compile('D')
        Sp = re.compile('S')

        for base in self.tResult.bases:
            qObject = {}
            qObject['base'] = parseBase(base)
            qObject['tableIndices'] = [0] * len(qObject['base'])
            qObject['pv'] = -1
            prob = -1 * self.tResult.bases[base]
            preterminal = ""
            
            for sB in qObject['base']:
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

            qObject['preterminal'] = preterminal
            qObject = (prob, qObject)
            # insert the q object into the pq
            self.pq.put(qObject)

    def printPq (self):

        row_format ="{:<}" + "{:>15}" * 4 + "{:>20}"
        print(row_format.format("",'Probability','Sub-Bases', 'Pre-terminal', 'Pivot Value','Indices'))

        while not self.pq.empty():
            qObject = self.pq.get()
            print(row_format.format("", '%.3f'%(-1 * qObject[0]), "".join(qObject[1]['base']), qObject[1]['preterminal'], qObject[1]['pv'], str(qObject[1]['tableIndices'])))
 


    def pqPopInsert(self):
        """Pop the highest probable pre-terminal struct from the queue"""



    


def main():
    print ("Please refer to README for usage and examples")

   
if __name__ == "__main__":
    main()