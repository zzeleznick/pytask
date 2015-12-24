import re
from itertools import chain
from collections import OrderedDict


stripper = lambda x,y: (x,y) if y else x

class odict(OrderedDict):
    """docstring for odict"""
    def __init__(self, name):
        super(odict, self).__init__()
        self.name = name
    def __repr__(self):
        items = self.items()
        items = [ stripper(i,j) for i,j in items]
        return '%s(%s)' % (self.name, items)

FILE = 'test3.zml' # 'test.zml'

nalpha = re.compile(r'[^a-zA-Z]')  # check for actual text
special_re = re.compile(r'(:{2}.?)') # starts with two colons
lvl_re = re.compile(r'\A:{1,}') # colons at start of line
depthfnc = lambda x: len((lvl_re.search(x)).group()) if lvl_re.search(x) else 0
conflict_msg = lambda c, d: '''Warning. Properties should not have the same name.
Found Conflicting name "%s" at depth %d.''' % (c,d)
null_parent_msg = lambda c: '''Child properties must be linked to a parent.
No parent properties found, but attempted to add "%s".''' % c
skipped_lvl_msg = lambda c,d: '''Tried to insert a child without a direct parent.
Found at depth %d with child %s''' % (d,c)

with open(FILE, 'r') as infile:
    lines = infile.readlines()

print lines
# scrub the file and only extract valid lines
valids = [ i for i, l in enumerate(lines) if len(nalpha.sub('', l)) > 0]
# each lines must be contain least one letter
lines = [lines[i] for i in valids]

properties = odict('properties')
# create an odict with name 'properties'
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
        assert len(prop) > 1, "Did not check valid lines correctly"
        depth = depthfnc(rawkey) - 2
        counter = depth
        # depthfnc -> number of lhs colons
        # # this allows for unbalanced as a feature ':::TEST::' still captured
        assert depth >= 0, "captured a non-special tag"
        count = len(properties) # number of root-level properties
        # parent will be node (count - 1), root-level will be 0
        if depth == 0 or not count: # root-level
            if prop in properties:
                print conflict_msg(prop, depth)
            properties[prop] = odict(prop)
            # insert property into properties, and initialize as odict with same name
        else:
            # this is a child of the parent
            assert count > 0, null_parent_msg(prop)
            # ensure there is a parent for this prop
            pkey = properties.keys()[count - 1]
            # retrieve the key of the parent
            parent = properties[pkey]
            # get the value of the parent
            while counter > 0:
                counter -= 1
                if counter == 0:
                    # this is a direct child
                    if prop in parent:
                        print conflict_msg(prop, depth)
                    parent[prop] = odict(prop)
                    # insert name of self into parent
                else:
                    length = len(parent)
                    if length > 0:
                        pkey = parent.keys()[length  - 1]
                        parent = parent[pkey]
                    else:
                        print skipped_lvl_msg(prop, depth)
                        parent[prop] = odict(prop)



print properties

'''
[ [data,[p1, [p2, [pp1, pp2]], p3]], [data2] ]
'''
