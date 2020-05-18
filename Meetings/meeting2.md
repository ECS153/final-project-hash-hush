# 5.10 meeting 2: 

## Data
Hashcode To be cracked:
    - HIBP SHA1 [hashes](https://haveibeenpwned.com/Passwords)
        -555278657 unique hashes 

Dictionaries: 
    - Rockyou: https://www.kaggle.com/wjburns/common-password-list-rockyoutxt
        - 14341564 unique passwords

## Steps
1.  Get Guesses
    1. PCFG/RNN:
        Input: Dictionaries/training set 
        Output: Guesses

    2. Hashcat Process: 
        - Dictionaries + Rules = Guesses

2. Guesses -> HashCode
3. Compare HashCode
4. Return Cracked hashcode: password


## Possibly conbinations

    - Rockyou Dictionaries -> success cases c1
    - Rockyou Dictionaries + PCFG -> Guesses -> success cases c2
    - Rockyou Dictionaries + NN -> Guesses -> success cases c3
    - Rockyou Dictionaries + Markov -> c4
    - Rockyou Dictionaries + best64 + …  -> c5
    


