"""An effective guess generation algo that generates guesses based on the training result"""

from queue import PriorityQueue

# tResult: the result of training
# finished: flag to indicate if the guesser has finished guessing 
#       1: deplete the guessing budget 
#       2: has tried all guesses
# guessingNumber: keep track of how many guesses has been generated
# pq: the priority queue that holds the pre-terminal structs

class GuessGen:
    """Generate guesses"""
    def __init__(self, budget, tResult):
        self.tResult = tResult
        self.finished = False
        self.guessingNumber = 0
        self.pq = PriorityQueue()

    def pqInit(self):
        """Initialize the priority Queue"""
        # A queue object:
        # (<prob>, {'base': <base struct>, 'preterminal': <preterminal struct>, 'pv': pivot value}, 'tableIndices': [])
        for base in self.tResult.bases:
            qObject = {}
            qObject['base'] = base
            prob = self.tResult.bases[base]


    def pqPopInsert(self):
        """Pop the highest probable pre-terminal struct from the queue"""















def main():
    print ("Please refer to README for usage and examples")

   
if __name__ == "__main__":
    main()