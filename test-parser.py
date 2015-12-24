import re
from itertools import chain
from collections import OrderedDict as odict

FILE = 'test.zml'

nalpha = re.compile(r'[^a-zA-Z]')  # check for actual text
special_re = re.compile(r'(:{2}.?)') # starts with two colons
lvl_re = re.compile(r'\A:{1,}') # colons at start of line
depthfnc = lambda x: len((lvl_re.search(x)).group()) if lvl_re.search(x) else 0
conflict_msg = lambda m: '''1st level properties must not have the same name.
Found Conflicting name "%s".''' % m
null_parent_msg = lambda m: '''Child properties must be linked to a parent.
No parent properties found, but attempted to add "%s".''' % m

with open(FILE, 'r') as infile:
    lines = infile.readlines()

print lines
# scrub the file and only extract valid lines
valids = [ i for i, l in enumerate(lines) if len(nalpha.sub('', l)) > 0]
# each lines must be contain least one letter
lines = [lines[i] for i in valids]

properties = odict()
for line in lines:
    iterator = special_re.finditer(line)
    matches = [ m.span() for m in iterator ]
    # gets all double colons, and we want the contents between
    limit = min(2, len(matches)) # force 1st match
    vals = range(1, limit, 2)    # for easy grouping
    hits = [(matches[i-1][0], matches[i][0]) for i in vals]
    if not hits: continue
    start, end = hits[0]
    special = line[start:end]
    # list of start and end characters for a property
    # should just take one per line
    if special:
        rawkey = special # the raw text including sp chars
        print rawkey
        prop = nalpha.sub('', rawkey).upper()
        # store them in A-Z only with clean, non-conflicting names
        depth = depthfnc(rawkey)
        # the depth (i.e. number of lhs colons)
        if depth == 2:
            assert len(prop) > 1, "Did not check valid lines correctly"
            old = properties.get(prop)
            if not old:
                properties[prop] = [] # list to store child props
            else:
                raise(IOError(conflict_msg(prop)))
        else:
            count = len(properties)
            assert count > 0, null_parent_msg(prop)
            parent = properties.keys()[count - 1]
            old = properties[parent]
            if not old:
                properties[parent] = [prop]
            else:
                properties[parent] = old + [prop]
print properties
