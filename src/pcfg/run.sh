#!/bin/zsh

# baseline model
hashcat -m 100 -O -a 0 ~/pwlists/hashes/pwned-SHA1-hashes-no-order.txt ~/pwlists/rockyou.txt -r ~/bin/hashcat/rules/best64.rule -o baseline.potfile

# pcfg (limit to 10 ^ 9 guesses)
python ~/153-project/src/pcfg/pcfg.py -b 1000000000 -l ~/153-project/src/pcfg/defaultRule hashcat -m 100 -O -a 0 ~/pwlists/hashes/pwned-SHA1-hashes-no-order.txt -o pcfgBillion.potfile