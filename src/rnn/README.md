# RNN Passwords generator 
Simple RNN that can be trained with passwords and then generate guesses. 

Sample training set: [rockyou.txt](https://www.kaggle.com/wjburns/common-password-list-rockyoutxt)

RNN credits from [Build RNN From Scratch](https://songhuiming.github.io/pages/2017/08/20/build-recurrent-neural-network-from-scratch/)
## pw_training.py
### TO RUN
  - pw_training.py -i <TrainingSet> -n <epochs|Optional> -o <offset|Optional>
    - **TrainingSet** must be an .txt
    - **epochs** must be a postive integer, Default is 10.
    - **offset** must be a postive integer. Default is 0. 
      The offset is for contiguous training. We are using sgd, sometimes one epoch takes a long time that 
      it could got interrupted. Number of training samples will be printed out, and you can use it to continue that epoch.
      U.npy, V.npy, W.npy will be updated every 1,000,000 training samples.
### FUNCTIONALITY 
Train the RNN with a <inputpassword.txt>. The RNN will learn about the features in this txt, and save the weights to U.npy, V.npy, W.npy
for future use. 
Hyperparameters can be set inside the code. 
  - Defalut learning rate is set to 0.05. 
  - Default Hidden Dimension is 100 (password of maxinum length 100). If changed, the hidden dimension in pw_guesses.py should also be changed.


## pw_guesses.py
### TO RUN
  - pw_guesses.py -o <outputfile> -n <numGuesses> -p <threshold|Optional>**
    - **output file** must be an .txt. For packing and convience, the outfile would be splited every 100,000,000 guesses.
      That is, if the out file is  out.txt  ,  the first 100,000,000 guesses would be stored in out_0.txt. Then out_1.txt, out_2.txt, etc.
    - **numGuesses** must be a postive integer, which is number of guesses you want to generate.
    - **threshold** must be a decimal between 0 and 1. We recommend it to be set below 0.5, if a threhold is high, it takes longer time to finish the tasks
      since passwords with probabilty lower than the threshold will be dumped.
### FUNCTIONALITY 
Generate guesses. There should be U.npy, V.npy, W.npy within the same directory, which would be used to caculate possiblity. 
