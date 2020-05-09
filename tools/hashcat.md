# HashCat 
- What are the options  
- A typical workflow of HashCat 

## Benchmark: -b
- `hashcat -b`: runs a benchmark on every hash mode
- `hashcat -b -m <mode>`: runs a benchmark on a specific hash type 

## Device to be used: -d, -D
- `-d`: followed by a list of integers separated by comma; specifies the device number to be used 
- `-D`: followed by a list of integers separated by comma; specifies the device type to be used
    - `1`: CPU
    - `2`: GPU
    - `3`: FPGA, DSP, Co-Processor

## `-O`: use hand optimized kernels
- hand optimized kernel is no longer by default
- has limit on the length of attempted guesses 

## `--stdout`: do not generate the hash, only displays the candidates on STDOUT
1. To ensure the rules are working 
2. To generate dictionaries by redirecting stdout to a file

## `--status-timer`: specifies the time gap between each display of status
- by default: 10 secs 
- `0`: not display the status at all
- `600`: every 10 mins


## [Intro to HashCat](https://www.youtube.com/watch?v=EfqJCKWtGiU&t=1s)
- The basic usage of Hashcat requires a minimum of 4 args 
1. `-m` or `--hash-type`
    - [Hash types/modes](https://hashcat.net/wiki/doku.php?id=example_hashes#legacy_hash_types) 
    - `100`: SHA-1

2. `-a` or `--attack-mode`: which cracking method to use 
    1. `0`: dictionary attack
    2. `1`: combination attack
    3. `3`: brute-force
    4. `6`: hybrid dictionary + mask
    5. `7`: hybrid mask + dictionary

3. file contains the hash tp be cracked or hash itself

4. dictionary/mask/directory to be used 

- eg: hashcat -m 100 -a ./hashes/sha-1s ./wordlists/rockyou.txt
    - the result is in `~/.hashcat/hashcat.potfile`

### Rules: `-r <rules>`

### Brute force: `-a 3`
- [can use a mask](https://www.unix-ninja.com/p/Exploiting_masks_in_Hashcat_for_fun_and_profit)
    - `?d`: place holder for a digit
    - `?l`: lower case letter 
    - `?u`: upper case letter
    - `?s`: special symbol
    - `?a`: all char sets 
    - also, custom char set is also possible 

- `-i`: enables mask increment mode

### Combination attack: `-a 1`
- takes two wordlists, parse and combine them

### Prince Attack, a advanced pw candidate generator 
- An utility NOT built into the hashcat
- let this utility to generate candidates first, then pipe the outputs to hashcat; hashcat will take input dictionary from *STDIN* instead of from an input file
- An improvement to combination attack
- rather than take two wordlist, princeprocessor takes one worlist and builds chains of combined words; can have 1 to N words from the input wordlist concatenated together
- princeprocessor can also take the output of another princeprocessor: prinception; 