# ECS 153 Project 

## Idea
1. generating more effective wordlists (minimize # of guesses)
    - in pw recovery case, users will supply their own info
    - in attacking scenario, we need to break/scan info 
2. generating more secure and usable pws or more secure auth protocol in general
    - randomly selecting word mangling rules to user chosen pws (susceptible to raking attack)
    - how websites add salts 
    - randomly choosing pw choosing rules mandated by the website
3. generating more effective word mangling rules
    - evaluating existing rules using real pws (how frequent the rules apply)
4. generate more effective dict/wordlist
    - the trade-off between the size of the dict and the number of mangling rules to tbe tried on them 
        - smaller dict and more rules are better at strong pws; large dict, fewer rules are better at weak pws 
        - To keep a dict not larger that it needed to be, use the best source: cracked pws
    - if the pw hashes are known to come from a particular site; what can we do 

## pw cracking Competition 
1. [crack me if you can](https://contest.korelogic.com/)
    - google `cmiyc writeup` for the behind the scene process in which the teams crack the hashes

2. [CracktheCon]
    - [2019](https://2019.crackthecon.com/)
    - again, can google the writeups

3. Crack this:
    - SHA1: d3839f0dc50133667906eee29b46bd8c69c9ce4f
    - SHA256: a9ccc6b792d00c391da1fc8258ab11b99385e6dec3e3d8351ea22c953e1d6e81

## Paper 
### Read 
1. Password Cracking: A Game of Wits
2. Password Cracking Using Probabilistic Context-Free Grammars
3. Testing Metrics for Password Creation Policies by Attacking Large Sets of Revealed Passwords

### To Read 
1. Fast Dictionary Attacks on Passwords Using Time-Space Tradeoff
2. Targeted Online Password Guessing: An Underestimated Threat
3. Fast, Lean, and Accurate: Modeling Password Guessability Using Neural Networks

## Book 
### read 

### To Read
1. Hash Crack - Password Cracking Manual (V2)
2. Hash Crack - Password Cracking Manual (V3)

## Video 
### Seen 
1.[Intro to hashcat, part I](https://www.youtube.com/watch?v=EfqJCKWtGiU)

### To See
2.[Intro to hashcat, part II](https://www.youtube.com/watch?v=FZ9g6Pau8ao&t=1s)

## Blogs 
### Read 

### To Read
1. [Weir's blog](https://reusablesec.blogspot.com/)
2. [PW complexity VS PW entrophy](https://docs.microsoft.com/en-us/archive/blogs/msftcam/password-complexity-versus-password-entropy)
3. [How Crypto Hash Works](https://www.metamorphosite.com/one-way-hash-encryption-sha1-data-software)


## Leaked wordlists & Dictionaries & Hashes 
### Wordlist & Dict
1. Rockyou leaked
2. Breachcompilation from [here](https://gist.github.com/scottlinux/9a3b11257ac575e4f71de811322ce6b3)
    - 1.4B original; 377 million unique, consists only of printable ascii chars
3. [Outpose9](http://www.outpost9.com/files/WordLists.html)
4. [CrackStation](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm)
    - a large one and a small one that only contains leaked pw
5. [SkullSecurity](https://wiki.skullsecurity.org/index.php?title=Passwords)
6. [weakpass](https://weakpass.com/wordlist)
7. [Capsop](https://wordlists.capsop.com/)
8. Unix-ninja DNA dict
9. [Probable wordlist](https://github.com/berzerk0/Probable-Wordlists)
10. [eff wordlist long](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt) & [short](https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt)
11. wikitionary 
12. 

### Hashes
1. HIBP SHA1 [hashes](https://haveibeenpwned.com/Passwords)

### Targeted Wordlists & Dict
1. [CEWL](https://github.com/digininja/CeWL/)
    - scrape keywords from websites
2. [Smeegescrape](https://github.com/SmeegeSec/SmeegeScrape)
    - scraper for text file and website
3. [LyricPass](https://github.com/initstring/lyricpass)
    - custom Dict generator using song lyrics 

## Tools 
1. STATSGEN: statistics about the wordlist

2. [ZXCVBN](https://github.com/dropbox/zxcvbn): PW strength estimation

3. [PIPAL & PASSPAT](https://github.com/digininja/pipal) 
    - PIPAL: PW Stats and pattern frequency analysis
    - PASSPAT: Keyboard pattern analysis



## Online PW analysis/research resources 
1. [Weakpass](http://weakpass.com/)

2. [Password Research](http://www.passwordresearch.com/)

3. [Hashes.org](https://hashes.org/)


## Rules & Masks
- [Hashcat & JtR](https://hashcat.net/wiki/doku.php?id=rule_based_attack)
- [PACK](https://github.com/iphelix/pack)

## Cracking SW

### HashCat
#### Advanced Attacking mode 
1. [Prince Attack](https://github.com/hashcat/princeprocessor)
2. [Mask Processor](https://github.com/hashcat/maskprocessor)
3. [Custom Markov Model](https://github.com/hashcat/statsprocessor)
4. [Keyboard Walk Processor](https://github.com/hashcat/kwprocessor)
5. Distributed Cracking


### John the Ripper 
#### Advanced Attacking Mode
1. Prince Attack
2. [Distributed Hacking](https://www.openwall.com/john/doc/OPTIONS.shtml)

### On-line Hash Cracking Services
1. [GPUhash](https://gpuhash.me/)
2. [CrackStation](https://crackstation.net/)
3. [Online Hash Crack](https://www.onlinehashcrack.com/)

## [PCFG cracker](https://github.com/lakiw/pcfg_cracker)

## [NN cracker](https://github.com/cupslab/neural_network_cracking)

## [Markov Chains](https://hal.archives-ouvertes.fr/hal-01112124/document)
