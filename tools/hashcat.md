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

## `-w <num>`: set workload profile 
1. low 
2. default 
3. high
4. Insane

## `--loop-back`: re-use the plains/passwords that did crack a hash
- e.g. apply some rules - after the first run - to the modified and matching plains. This kind of looping will only stop if no more plains match.

## `-j`, `-k`: takes 2 dicts, applies single rule to one of the dicts 
- `-j`: apply one rule to the left dict
- `-k`: apply one rule to the right dict 

## `-o` <file>: output result to file 

## `--session <str>`: name the session

## `--restore --session <str>`: restore session with name <str>;
- `--session <str>` is optional 

## `-g <num>`: generate num random rules

## [Intro to HashCat](https://www.youtube.com/watch?v=EfqJCKWtGiU&t=1s)
- The basic usage of Hashcat requires a minimum of 4 args 
1. `-m` or `--hash-type`
    - [Hash types/modes](https://hashcat.net/wiki/doku.php?id=example_hashes#legacy_hash_types) 
    - `100`: SHA-1

2. `-a` or `--attack-mode`: which cracking method to use 
    1. `0`: dictionary attack
    2. `1`: combination attack
    3. `3`: brute-force
    4. `6`: hybrid dictionary + mask (appending masks)
    5. `7`: hybrid mask + dictionary (prepending masks)

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
    - `-1`, `-2`, `-3`, `-4` followed by the custom char set
        - eg: use hex char set stored in `-1` buffer as mask: `-1 ?dabcdefABCDEF c6?1?1?1?d?1` (`?d` automatically sub for `123456890`, we know this pws starts with `c6` and the second to last char is a digit)

- `-i`: enables mask increment mode

### Combination attack: `-a 1`
- takes two wordlists, parse and combine them

### Prince Attack, a advanced pw candidate generator 
- An utility NOT built into the hashcat
- let this utility to generate candidates first, then pipe the outputs to hashcat; hashcat will take input dictionary from *STDIN* instead of from an input file
- An improvement to combination attack
- rather than take two wordlist, princeprocessor takes one worlist and builds chains of combined words; can have 1 to N words from the input wordlist concatenated together
- princeprocessor can also take the output of another princeprocessor:
  prinception

