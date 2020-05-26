import sys, getopt
import numpy as np
import numpy
import itertools
import operator
from datetime import datetime


# credit from https://songhuiming.github.io/pages/2017/08/20/build-recurrent-neural-network-from-scratch/

def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)

'''
 - model:
 - X_train:
 - y_train:
 - learning_rate:
 - nepoch:
 - evaluate loss_after:
'''

def train_with_sgd(model, X_train, y_train, learning_rate = 0.05, nepoch = 100, evaluate_loss_after = 5):
    # keep track of the losses so that we can plot them later
    losses = []
    num_examples_seen = 0
    for epoch in range(nepoch):
        # for each training example...
        print(str(epoch) + "th epoch:")
        sys.stdout.flush()

        for i in range(len(y_train)):
            # one sgd step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1
            if(num_examples_seen % 1000000 == 0):
                print("    " + str(num_examples_seen))
                sys.stdout.flush()
                
                np.save('U.npy', model.U)
                np.save('V.npy', model.V)
                np.save('W.npy', model.W)

        
        np.save('U.npy', model.U)
        np.save('V.npy', model.V)
        np.save('W.npy', model.W)
        
        # optionally evaluate the loss
        if (epoch % evaluate_loss_after == 0):
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            print("loss after num_examples_seen=%d epoch=%d: %f" %(num_examples_seen, epoch, loss))
            # adjust the learning rate if loss increases
            if (len(losses) > 1 and losses[-1][1] > losses[-2][1]):
                learning_rate = learning_rate * 0.5
                print("setting learning rate to %f" %(learning_rate))
            sys.stdout.flush()
        
        
class RNNNumpy():
    def __init__(self, word_dim, hidden_dim = 100, bptt_truncate = 4, continued = False):
        # assign instance variable
        self.word_dim = word_dim   # number of possible characters, in this case 86
        self.hidden_dim = hidden_dim # number of hidden units
        self.bptt_truncate = bptt_truncate
            
        if(continued):
            print("read in previous weights")
            sys.stdout.flush()
            try:
                self.U = np.load("U.npy")
                self.V = np.load("V.npy")
                self.W = np.load("W.npy")
            except IOError:
                self.U = np.random.uniform(-np.sqrt(1./word_dim), np.sqrt(1./word_dim), (hidden_dim, word_dim))
                self.V = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (word_dim, hidden_dim))
                self.W = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (hidden_dim, hidden_dim))
        else:
            # random initiate the parameters
            self.U = np.random.uniform(-np.sqrt(1./word_dim), np.sqrt(1./word_dim), (hidden_dim, word_dim))
            self.V = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (word_dim, hidden_dim))
            self.W = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (hidden_dim, hidden_dim))
    
    def forward_progagation(self, x):
        # total time steps / length of the password
        T = len(x)

        #intialize s, with the initial state s set to zero, we thus have T+1 rows, each with size of hidden_dim
        s = np.zeros((T+1, self.hidden_dim))
        #intialize o,
        o = np.zeros((T, self.word_dim))

        
        for t in numpy.arange(T):
            # since x is a one-hot encoder, index U with x[t] is the same thing as mutiply U with tons of 0s
            
            s[t] = np.tanh(self.U[:, x[t]] + self.W.dot(s[t-1]))
            o[t] = softmax(self.V.dot(s[t]))
        return [o, s]

    def predict(self, x):
        o, s = self.forward_progagation(x)
        return np.argmax(o, axis = 1)
        
        
    # in this case x and y are 2-d arrays
    def calculate_total_loss(self, x, y):
        L = 0
        # for each sentence ...
        for i in numpy.arange(len(y)):
            o, s = self.forward_progagation(x[i])
            # we only care about our prediction of the "correct" words
            correct_word_predictions = o[numpy.arange(len(y[i])), y[i]]
            # add to the loss based on how off we were
            L += -1 * np.sum(np.log(correct_word_predictions))
        return L

    # in this case x and y are 2-d arrays
    def calculate_loss(self, x, y):
        # divide the total loss by the number of training examples
        N = np.sum((len(y_i) for y_i in y))
        return self.calculate_total_loss(x, y)/N
      
    def bptt(self, x, y):
        T = len(y)
        # perform forward propagation
        o, s = self.forward_progagation(x)
        # we will accumulate the gradients in these variables
        dLdU = np.zeros(self.U.shape)
        dLdV = np.zeros(self.V.shape)
        dLdW = np.zeros(self.W.shape)
        delta_o = o
        delta_o[numpy.arange(len(y)), y] -= 1   # it is y_hat - y
        # for each output backwards ...
        
        
        for t in numpy.arange(T):
            dLdV += np.outer(delta_o[t], s[t].T)    # at time step t, shape is word_dim * hidden_dim
            # initial delta calculation
            delta_t = self.V.T.dot(delta_o[t]) * (1 - (s[t] ** 2))
            # backpropagation through time (for at most self.bptt_truncate steps)
            # given time step t, go back from time step t, to t-1, t-2, ...
            for bptt_step in numpy.arange(max(0, t-self.bptt_truncate), t+1)[::-1]:
                # print("Backprogation step t=%d bptt step=%d" %(t, bptt_step))
                dLdW += np.outer(delta_t, s[bptt_step - 1])
                dLdU[:, x[bptt_step]] += delta_t
                # update delta for next step
                dleta_t = self.W.T.dot(delta_t) * (1 - s[bptt_step-1]**2)
        return [dLdU, dLdV, dLdW]
        

    def sgd_step(self, x, y, learning_rate):
        dLdU, dLdV, dLdW = self.bptt(x, y)
        self.U -= learning_rate * dLdU
        self.V -= learning_rate * dLdV
        self.W -= learning_rate * dLdW


# around 70 secs for rockyou.txt
# https://theasciicode.com.ar/ascii-control-characters/backspace-ascii-code-8.html
# set range for char 32 - 126 in ascii,  95 chars, remove any pw cotains char outside the range
# also we want an addtional char START and END indicates the start and end of the password, so totally 97 chars
# END would only appear in y, START only in x

def generate_training_pw(infile):
    f = open(infile, "r", errors='ignore')
    line = f.readline()
    x = []
    y = []
    count = 0
    while line != "":
        l = [ord(i)-31 for i in line][:-1] # convert to int
        if any(y > 95 or y < 1 for y in l):
            line = f.readline()
            continue
        l.insert(0, 0)
        x.append(l) # add to X

        l.append(96)
        l = l[1:]
        y.append(l) # modify and add to y
        line = f.readline()

        #count
        count = count+1
        if(count % 1000000 == 0):
            print(str(count / 1000000) + "million")
    print("Finished with " + str(count) + " passwords")
    return x,y


# -----------------------------------------RUN SCRIPT-----------------------------------------------

input = sys.argv[1:]

offset = 0
epochs = 10
inputfile = ""

try:
    opts, args = getopt.getopt(input,"i:n:o:")
except getopt.GetoptError:
    print("pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>")
    sys.exit(2)
    
for opt, arg in opts:
    if opt == "-i" :
        if ".txt" not in arg:
            print("Error: TrainingSet must be a txt.")
            print("pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>")
            sys.exit(2)
            
        inputfile = arg
    elif opt == "-n":
        try:
           epochs = int(arg)
        except ValueError:
           print("Error: Epochs must be integer")
           print("pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>")
    elif opt == "-o":
        try:
           offset = int(arg)
        except ValueError:
           print("Error: Offset must be integer")
           print("pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>")

if(inputfile == ""):
    print("Error: Must have a training set.")
    print("pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>")
    sys.exit(2)

#print(offset)
#print(epochs)
#print(inputfile)


# 1. load in file
print("load in " + inputfile)
x, y = generate_training_pw(inputfile)

# 2. initialize
np.random.seed(10)
char_size = 97

# 3. if offset is not zero, continue the learning session from last time
model = RNNNumpy(char_size, continued =True)

if(offset != 0):
    model = RNNNumpy(char_size, continued =True)
    #finsh up this epoch first
    print("finish up previous epoch")
    losses = train_with_sgd(model, x[offset:], y[offset:], nepoch = 1)

# 4. training RNN
print("new training")
losses = train_with_sgd(model, x, y, nepoch = epochs, evaluate_loss_after = 2)


# 5. TODO: Generate random passwords -> check for validty -> caculate probability -> compare with threhold -> throw away or store
