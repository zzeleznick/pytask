import re
from itertools import chain
from collections import OrderedDict as odict

FILE = 'test.zml'

with open(FILE, 'r') as infile:
    lines = infile.readlines()

print lines
# scrub the file and only extract valid lines

nalpha = re.compile(r'[^a-zA-Z]')  # check for actual text
valids = [ i for i, l in enumerate(lines) if len(nalpha.sub('', l)) > 0]
# each lines must be contain least one letter
lines = [lines[i] for i in valids]
# new_list = list(chain(a[0:2], [a[4]], a[6:]))
special = re.compile(r'(:{2}.?)') # starts with two colons

properties = odict()
for line in lines:
    iterator = special.finditer(line)
    matches = [ m.span() for m in iterator ]
    # get all double colons
    limit = min(2, len(matches))
    vals = range(1, limit, 2)
    groups = [(matches[i-1][1]-1, matches[i][0]) for i in vals]
    # take the end of 1st dbl colon and start of next
    if lst:
        prop = [line[b:e] for i, (b,e) in enumerate(lst) if i == 0 ][0]
        # get the first matching property
        print 'Dirty matches', prop
        prop = nalpha.sub('', prop) # properties must be alpha only
        print 'Clean matches', prop
        if prop:
            properties += [prop]
print properties
