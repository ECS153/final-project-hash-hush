#!/bin/zsh

# Testing pw generators:
## pull 1000 random samples from rockyou.txt for testing 
# shuf -n 1000 ~/pwlists/rockyou.txt > test 

# shuf -n 100000 ~/pwlists/hashes/pwned-SHA1-hashes-no-order.txt > testHashes2



# Breaking big hash file into small chunks so that each chunk can fit into (video) memory
# split -l 23136611 $FileName hibp
## output: hibpaa, hibpab, hibpac, ..., hibpau, hibpaw, hibpax (24 files)
## 555278657 / 24 = 23136610.7 (lines/hashes per file)

# baseline model(s)
# 1: rockyou.txt + best64.rule
# 1). generate guesses
hashcat -O --stdout -r ~/bin/hashcat/rules/best64.rule ~/pwlists/rockyou.txt > ~/pwlists/rockyouBest64.txt

## rockyouBest64.txt has 1104517645 guesses

# 2). try them on all hash subsets 
for f in ~/pwlists/hashes/hibpa*
do ~/bin/hashcat/hashcat -m 100 -O -a 0 $f ~/pwlists/rockyouBest64.txt -o baseline.potfile
done

# 2: dict0294.txt + best64.rule



# pcfg (limit to 10 ^ 9 guesses)

## Train and guess 
python ~/153-project/src/pcfg/pcfg.py -d ~/pwlists/rockyou.txt ~/pwlists/dic-0294.txt -b 100 > t

## train 
python ~/153-project/src/pcfg/pcfg.py -s defaultRule -d ~/pwlists/rockyou.txt ~/pwlists/dicdna.txt 
##  dicdna.txt = dic-0294.txt + dna.txt

## guess 
python ~/153-project/src/pcfg/pcfg.py -b 1104517645 -l ~/153-project/src/pcfg/defaultRule > ~/pwlists/pcfgGuesses.txt

## guess and debug
python ~/153-project/src/pcfg/pcfg.py -b 1104517645 -l ~/153-project/src/pcfg/defaultRule > ~/pwlists/pcfgGuesses.txt >2 status.txt

for f in ~/pwlists/hashes/hibpa*
do ~/bin/hashcat/hashcat -m 100 -O -a 0 $f ~/pwlists/pcfgGuesses.txt -o pcfgBillion$f.potfile
done

# # demo 
# python ~/153-project/src/pcfg/pcfg.py -b 10000 -l ~/153-project/src/pcfg/defaultRule | hashcat -m 100 -O -a 0 ~/153-project/src/pcfg/testHashes -o demo.potfile