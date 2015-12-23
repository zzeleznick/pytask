from collections import OrderedDict as odict

# file for creating config
import os
import csv

"""
At a high-level, every task list should be a container
of tasks, whose properties are not inferred other than
a way to add, remove, and sort

- define a task generally (schema)
    - define any number of type of fields
- define a csvfile I/O
    - encode all task information per line
- handle tasklist methods
- provide generics
"""

iterReq = lambda d, x: "Arg '%s' of %s must be iterable." % (d, type(x))
sameLengthReq = lambda x, y: 'Fields (%d) and Types (%d) must have same length.' % (len(x), len(y))
CMD = lambda x: x.strip().upper()
checkHelp = lambda x: 1 if (CMD(x) == 'H' or CMD(x) == 'HELP') else 0
checkExit = lambda x: 1 if (CMD(x) == 'X' or CMD(x) == 'Q' or CMD(x) == 'QUIT') else 0
checkUndo =  lambda x: 1 if (CMD(x) == 'B' or CMD(x) == 'U' or CMD(x) == 'UNDO') else 0

class Command(object):
    def __init__(self, text):
        self.text = text
    def is_help(self):
        return checkHelp(self.text)
    def is_undo(self):
        return checkUndo(self.text)
    def is_exit(self):
        return checkExit(self.text)

class Schema(object):
    """docstring for Schema"""
    def __init__(self, fields, expected_types, defaults = []):
        self.null = ''
        self.name = 'Schema'

        self.fields = fields
        self.expected = odict([(name,t)  for name, t in zip(fields, expected_types)])
        self.check_expected()

        defaults = self.build_defaults(fields, defaults)
        self.defaults = odict([(name,v)  for name, v in zip(fields, defaults)])
        self.check_internals(self.defaults)

        self.values = odict([(name,'')  for name, v in zip(fields, defaults)])
        # each field has a key of name, and value of order in the dict

    def populate(self, name):
        self.fill_field(name)

    def populate_all(self):
        for name in self.values:
            val = self.values[name]
            if not val:
                self.populate(name)

    def check_internals(self, internals, raisesError = True):
        """Test we built internals correctly"""
        for name in internals:
            val = internals[name]
            if not self.is_valid(name, val) and raisesError:
                raise(self.is_valid(name, val, returnError = True))
            elif not self.is_valid(name, val):
                return False
        else:
            return True

    def check_expected(self):
        fds = self.fields
        exp = self.expected
        assert '__iter__' in dir(fds), iterReq('fields', fds)
        assert '__iter__' in dir(exp), iterReq('expected_types', exp)
        assert len(fds) == len(exp), sameLengthReq(fds, exp)
        return True

    def build_defaults(self, fields, defaults):
        """Assume it works, then test if it works"""
        assert '__iter__' in dir(defaults), iterReq('defaults', defaults)
        if defaults:
            if len(defaults) != len(fields):
                defaults = [defaults[0]]* len(fields)
        else:
            defaults = [self.null] * len(fields)
        return defaults

    def is_valid(self, name, value, returnError = False):
        """Checks a value for type validity from the expected Types"""
        convert = self.expected[name]
        try:
            parsed = convert(value)
        except Exception, e:
            if returnError:
                return e
            else:
                return False
        else:
            return True

    def fill_field(self, name, value = None, throwError = False):
        """At this point, all default values are of correct type"""

        if self.is_valid(name, value):
            convert = self.expected[name]
            converted = convert(value)
            self.values[name] = converted
        elif throwError:
             raise(self.is_valid(name, value, returnError = True))
        else:
            if value:  # wasn't valid, but inputted
                self.values[name] = self.null
            else:
                self.values[name] = self.defaults[name]

    def __repr__(self):
        head = '|--=s %s s=--|' % self.name
        end =  '|--=e %s e=--|' % self.name
        fields = ["'%s': %s" % (k, self.values[k]) for k in self.values]
        expected = ["%s" % (self.expected[k]) for k in self.expected]
        pairs = zip(fields, expected)
        lines = [', '.join(pair) for pair in pairs]
        return '\n'.join([head, '\n'.join(lines), end])
    def __str__(self):
        return repr(self)

class Form(Schema):
    """docstring for Form"""
    def __init__(self, fields, expected_types, defaults = [],
                 promptFncs = [], helpFncs = []):
        super(Form, self).__init__(fields, expected_types, defaults)
        self.name = 'Form'
        self._prompt = lambda x,y: lambda: "Enter a %s into field '%s'" % (x,y)
        self._help = lambda x,y: lambda: '<insert> value into %s' % (y)
        self.prompts = self.buildHelpMessages(promptFncs, fallback = self._prompt )
        self.helpers = self.buildHelpMessages(helpFncs, fallback = self._help )
        self.incomplete = self.checkForMissingValues
        self.counter = 0

    def buildHelpMessages(self, helpFncs, fallback):
        if not helpFncs:
            # i.e. empty list
            helpFncs = [ fallback(self.expected[k], k) for k in self.expected]
        fncs = self.build_defaults(self.fields, helpFncs)
        fncDict = odict( [(name, fn)  for name, fn in zip(self.fields, fncs)] )
        return fncDict

    def checkForMissingValues(self):
        for key in self.values:
            if self.values[key] == self.null:
                return True
        return False

    def prompt(self, name):
        return self.prompts[name]()

    def all_prompts(self):
        for name in self.values:
            print self.prompt(name)

    def help(self, name):
        return self.helpers[name]()

    def all_help(self):
        for name in self.values:
            print self.help(name)

    def consumeInput(self):
        """
        INFO: Main Method to walk users through filling out all required fields.
        NOTES:
            - if user input maps to exit, exits
            - if user input maps to help, displays help
            - if user input maps to undo, resets last input
        """
        raw = raw_input()
        idx = self.counter
        name = self.values.keys()[idx]
        cmd = Command(raw)
        if cmd.is_exit():
            print 'Exit triggered'; exit()
        elif cmd.is_help():
            print self.help(name)
        elif cmd.is_undo():
            self.counter = max(0, self.counter - 1)
            name = self.values.keys()[self.counter]
            self.values[name] = self.null
        else:
            self.fill_field(name, raw)
            out = self.values[name]
            if out:
                print "Adding %s to field '%s'." % (out, name)
                self.counter += 1

    def proccess(self):
        while self.incomplete():
            # print 'Counter at', self.counter
            name = self.values.keys()[self.counter]
            print self.prompt(name)
            self.consumeInput()
        return self.values.values()

class Task(Schema):
    """docstring for Task"""
    def __init__(self, arg):
        super(Task, self).__init__()
        self.arg = arg

class TaskDefault(Task):
    """docstring for TaskDefault"""
    def __init__(self, arg):
        super(TaskDefault, self).__init__()
        self.arg = arg




class DataStore(object):
    """docstring for PriorityLevel"""
    def __init__(self, vals):
        zvals = self.build(vals)
        self.DATA_FOLDER = zvals[0]
        self.CURRENT_TASKS = zvals[1]
        self.COMPLETED_TASKS = zvals[2]
        self.DELETED_TASKS = zvals[3]
        self.getVals = lambda: [self.DATA_FOLDER, self.CURRENT_TASKS,
                                self.COMPLETED_TASKS, self.DELETED_TASKS]
        self.load = self.loadCurrentTasks
        self.write = self.writeTask
    def build(self, vals):
        if vals and type(vals) == list and len(vals) >= 4:
            VALS = vals
        else:
            favorite = '/Users/zeleznick/tasker/'
            try:
                os.chdir(favorite)
            except Exception, e:
                pass
            VALS = [ 'data/', 'CURRENT.csv',
                    'COMPLETED.csv', 'DELETED.csv']
        if not os.path.isdir(VALS[0]):
            print 'DATA_FOLDER %s not on path. Creating now...' % VALS[0]
            os.mkdir(VALS[0])
        for name in VALS[1:]:
            if name not in os.listdir(VALS[0]):
                f = open(VALS[0] + name, 'w')
                f.close()
        return VALS

    def loadCurrentTasks(self):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'rb') as infile:
            reader = csv.reader(infile, delimiter='@')
            out = [row for row in reader] # list of list of strings
        return out

    def dumpTasks(self):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        f = open(fname, 'w')
        f.close()

    def writeTasks(self, taskList):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'a') as csvfile:
            zwriter = csv.writer(csvfile, delimiter='@',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for idx, key in enumerate(taskList.tasks):
                t1 = taskList.tasks[key]
                desc, value, due, created = [t1.description, t1.priority.value, t1.due.hrep, t1.created.hrep]
                zwriter.writerow([created] + [desc] + [value] + [due])

    def writeTask(self, desc, value, created, due):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'a') as csvfile:
            zwriter = csv.writer(csvfile, delimiter='@',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            zwriter.writerow([created] + [desc] + [value] + [due])
    def __repr__(self):
        return '<DS %s | %s>' % (self.DATA_FOLDER, self.CURRENT_TASKS)
    def __str__(self):
        return repr(self)

def buildConfig(zvals = []):
    ds = DataStore(zvals)
    return ds

def test_Schema():
    fields = ['desc', 'value', 'date']
    expected = [str, int, str]
    defaults = ['x', 1, 'y']
    schema = Schema(fields, expected, defaults)
    print schema
    schema.populate_all()
    print schema

def test_FormH():
    fields = ['desc', 'value', 'date']
    expected = [str, int, str]
    defaults = ['x', 1, 'y']
    # helpFn = lambda x: lambda: '<insert> value into %s' % x
    # helpers = [helpFn(el) for el in fields]
    helpers = []
    form = Form(fields, expected, defaults, helpers)
    print form
    print 'Help:'
    form.all_help()
    print 'Prompts:'
    form.all_prompts()

def test_FormI():
    fields = ['desc', 'value', 'date']
    expected = [str, int, str]
    defaults = ['x', 1, 'y']
    form = Form(fields, expected, defaults)
    vals = form.proccess()
    print vals

if __name__ == '__main__':
    # test_Schema()
    test_FormH()
    test_FormI()