import re
from itertools import chain
from collections import OrderedDict


class MyObject(object):
    """docstring for Myobject"""
    def __init__(self, name = 'Myobject'):
        super(MyObject, self).__init__()
        self.name = name
    def set_prop(self, field, value, expected_type = str):
        try:
            converted = expected_type(value)
        except Exception, e:
            raise(e)
        else:
            self.__dict__[field] = converted
    def __repr__(self):
        items = self.__dict__
        return '%s(%s)' % (self.name, items)

class odict(OrderedDict):
    """docstring for odict"""
    def __init__(self, name, depth = 0):
        super(odict, self).__init__()
        self.name = name
        self.depth = depth
        self.stripper = lambda x,y: y if y else x
    def __repr__(self):
        items = self.items()
        items = [ self.stripper(i,j) for i,j in items]
        indents = '\n' + ':' * (self.depth + 2)
        return '%s%s(%s)' % (indents, self.name, items)

FILE = 'test.zml'

# |---== REGEX EXPRESSIONS ==---|
nalpha = re.compile(r'[^a-zA-Z]')  # check for actual text
alphad = re.compile(r'[^a-zA-Z0-9]')
special_re = re.compile(r'(:{2}.?)') # starts with two colons
lvl_re = re.compile(r'\A:{1,}') # colons at start of line

# |---== HELPER FUNCTIONS ==---|
depthfnc = lambda x: len((lvl_re.search(x)).group()) if lvl_re.search(x) else 0
# this allows for unbalanced as a feature ':::TEST::' still captured

# |---== HELP MESSAGES ==---|
conflict_msg = lambda c, d: '''WARN: Properties should not have the same name.
Found Conflicting name "%s" at depth %d.\n''' % (c,d)

null_parent_msg = lambda c: '''Child properties must be linked to a parent.
No parent properties found, but attempted to add "%s".''' % c

skipped_lvl_msg = lambda c,d: '''Tried to insert a child without a direct parent.
Found at depth %d with child %s''' % (d,c)

def get_hits(regex, line):
    '''
    Using a regular expression, returns the grouped contents
    between two hits of the desired special character delimiter.
    The LHS is kept with the contents, whereas the RHS delimiter
    is discarded, to allow for unbalanced use cases

    i.e. looking for '::' at the start and end of a contained word
         'junk::STUFF::morejunk:;bpah::' --> ::STUFF
    '''
    iterator = regex.finditer(line)
    matches = [ m.span() for m in iterator ]
    # gets all double colons, and we want the contents between
    limit = min(2, len(matches)) # force 1st match
    vals = range(1, limit, 2)    # for easy grouping
    hits = [(matches[i-1][0], matches[i][0]) for i in vals]
    if hits:
        start, end = hits[0]
        special = line[start:end]
        return special
    else:
        return None

def get_lines(filename):
    ''' Returns the lines of a file.'''
    with open(filename, 'r') as infile:
        lines = infile.readlines()
    return lines

def get_properties(lines):
    '''
    Properties as indicated by their grouping inside special delimiters
    are captured, their text is stripped of non-alpha numeric characters.

    Depth (distance from root) is calculated from the number of colons
    that appear on the left-hand side (LHS) of a property.
    LHS does not need to equal RHS, but each must be greater than 2
    to trigger their contained word as a property.
    '''
    # scrub the file and only extract valid lines
    valids = [ i for i, l in enumerate(lines) if len(alphad.sub('', l)) > 0]
    # each lines must be contain least one letter
    lines = [lines[i] for i in valids]
    properties = odict('properties') # create an odict with name 'properties'
    for line in lines:
        rawkey = get_hits(special_re, line)
        if not rawkey:
            continue
        # print rawkey
        prop = alphad.sub('', rawkey)
        # assert len(prop) > 1, "Did not check valid lines correctly"
        depth = depthfnc(rawkey) - 2
        # assert depth >= 0, "captured a non-special tag"
        counter = depth
        roots = len(properties) # number of root-level properties
        # |---== PROPERTY IS AT ROOT LEVEL==---|
        if depth == 0 or not roots: #
            if prop in properties:
                print conflict_msg(prop, depth)
            properties[prop] = odict(prop) # insert prop into properties; initialize new odict
            # |---== OTHERWISE PROPERTY IS CHILD OF A ROOT ==---|
            continue
        # assert roots > 0, null_parent_msg(prop) # ensure there is a parent for this prop
        # |---== GET PARENT AND GO  ==---|
        pkey = properties.keys()[roots - 1]
        parent = properties[pkey]
        while counter > 0:
            counter -= 1
            # |---== PROPERTY IS DIRECT CHILD ==---|
            if counter == 0:
                if prop in parent:
                    print conflict_msg(prop, depth)
                parent[prop] = odict(prop, depth)  # insert name of self into parent
            # |---== ELSE: TRAVERSE THE TREE  ==---|
            else:
                length = len(parent)
                # |---== GET THE CLOSER PARENT AND SET AS ROOT  ==---|
                if length > 0:
                    pkey = parent.keys()[length  - 1]
                    parent = parent[pkey]
                # |---== ELSE: PREMATURELY ADD, SINCE TREE ENDS ==---|
                else:
                    print skipped_lvl_msg(prop, depth)
                    parent[prop] = odict(prop, depth)

            # end of adding a deep property
        # end of adding a potential property to a line
    # end of all lines
    return properties

def parseZML(filename):
    lines = get_lines(filename)
    print ''.join(lines)
    props = get_properties(lines)
    print props
    return props

def test():
    lines = ['::Fields::', ':::name::', ':::value::', ':::lst::',
    '::Types::', ':::str::', ':::int::', ':::list::',
    '::Values::', ':::Zach::', ':::2::', ':::shit::' ]
    props = get_properties(lines)
    print props, '\n'
    lst = []
    for k in props.keys():
        print '|---==%s==---|' % (k)
        od = props[k]
        sublist = []
        for key in od:
            sublist += [key]
        print sublist, '\n'
        lst += [sublist]
    fields, exp, vals = lst
    print lst
    assert len(fields) == len(exp) and len(exp) == len(vals)
    namespace = zip(fields, vals, exp)
    out = MyObject()
    for f,v,e in namespace:
        tp = eval(e)
        out.set_prop(f,v,tp)

    print out


if __name__ == '__main__':
    # parseZML(FILE)
    test()