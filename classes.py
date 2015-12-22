import sys
import time
import copy as cp
import re
from collections import OrderedDict as odict

from termcolor import colored # coloring yay
from datetime import datetime as dt
# internals
from utils import *

EPOCH = dt.fromtimestamp(0)
colors = ["blue", "green", "yellow", "red"]
names = ["Default", "Easy", "Medium", "Hard"]
edges =  [0, 2, 3, 5]
mycolor = lambda x: colors[sorted(edges + [x]).index(x)]
myname = lambda x: names[sorted(edges + [x]).index(x)]

class FormFiller(object):
    """docstring for FormFiller"""
    def __init__(self, null = ''):
        self.null = null
        self.incomplete = self.checkForMissingValues
        self.counter = 0
        self.fields = odict()
        self.defaults = odict()
        self.help = odict()
        self.count = lambda: len(self.fields)

    def checkForMissingValues(self):
        for key in self.fields:
            if self.fields[key] == self.null:
                return True
        return False

    def setField(self, name, value, soft_exit = False):
        convert = self.defaults[name][0]
        try:
            parsed = convert(value)
        except Exception, e:
            if soft_exit: print e
            else: raise(e)
        else:
            self.fields[name] = parsed
            self.counter += 1

    def addRequiredField(self, name, expected = str, default = '', helptext = '', helpfnc = lambda: ''):
        if not default:
            default = self.null
        if not helptext:
            helptext = "Enter %s for '%s'." % (type(default), name)
        self.fields[name] = self.null
        self.defaults[name] = (expected, default)
        self.help[name] = (helptext, helpfnc)

    def runHelpFnc(self, idx):
        key = self.fields.keys()[idx]
        return self.help[key][1]()

    def getPrompt(self, idx):
        key = self.fields.keys()[idx]
        return self.help[key][0]

    def requestInput(self, idx):
        print self.getPrompt(idx)

    def consumeInput(self):
        raw = raw_input()
        idx = self.counter
        key = self.fields.keys()[idx]
        checkExit(raw)
        if checkHelp(raw):
            print self.runHelpFnc(idx)
        elif checkUndo(raw):
            self.counter = max(0, self.counter - 1)
            key = self.fields.keys()[self.counter]
            self.fields[key] = self.null
        elif not raw:
            cached = self.defaults[key][1]
            if cached:
                self.setField(key, cached, soft_exit = True)
        else:
            self.setField(key, raw, soft_exit = True)

    def proccess(self):
        while self.incomplete():
            # print 'Counter at', self.counter
            self.requestInput(self.counter)
            self.consumeInput()
        return self.fields.values()

    def __repr__(self):
        return '<Form with fields %s>' % self.fields.keys()

    def __str__(self):
        head = '--Begin Form--'
        end = '--End Form--'
        fields = ["'%s': %s" % (name, val) for name, val in self.fields.items()]
        print self.defaults.values()
        defaults = ["%s, default: '%s'" % (exp, val) for exp, val in self.defaults.values()]
        pairs = zip(fields, defaults)
        lines = [', '.join(pair) for pair in pairs]
        return '\n'.join([head, '\n'.join(lines), end])


class PriorityLevel(object):
    """docstring for PriorityLevel"""
    __high = 5
    __low = 0
    def __init__(self, val, colored = True):
        # super(PriorityLevel, self).__init__()
        # input value can 0-5,
        # { 0: [0, blue, unset], 1: [1-2, green, easy],
        # 2: [3, yellow, med],  3: [4-5: red, hard]}
        self.colored = colored  # whether returned string is colored
        high = PriorityLevel.__high
        low = PriorityLevel.__low
        def setValue(val):
            if type(val) != int: # if val is passed in as a string
                try: val = int(val) # attempt conversion
                except Exception, e: val = low # 0 if failed
            val = min(max(val, low), high)
            return val % (high+1)
        self.value = setValue(val) # 1-5 for valid
        self.color = mycolor(self.value)  # color
        self.name = myname(self.value)  # name of label
        self.rep = '%s %d' % (self.name, self.value)
        self.hrep = '*' * (self.value) + ' ' * (high - self.value)

    def __repr__(self):
        return '<%s Label>' % self.rep

    def __str__(self):
        if self.colored:
            return colored(self.hrep, self.color)
        else:
            return self.hrep


class Timestamp(object):
    """docstring for Timestamp"""
    def __init__(self, date = None, d_offset = 0, h_offset = 0, m_offset = 0):
        # super(Timestamp, self).__init__()
        t = dt.now() if not date else date
        offset = (((d_offset * 24 + h_offset) * 60) + m_offset)  * 60
        self.value = int((t - EPOCH).total_seconds()) + offset # raw seconds since epoch
        self.date = dt.fromtimestamp(self.value) # date object
        self.rep = dt.strftime(self.date, "%Y-%m-%d %H:%M:%S") # created
        self.hrep = dt.strftime(self.date, "%a %b %d, %Y at %I:%M %p") # human readable created
    def asDate(self):
        return self.date
    def as24hour(self):
        return self.rep
    def __repr__(self):
        return '<TS %s>' % self.rep
    def __str__(self):
        return self.hrep

class Task(object):
    """docstring for Task"""
    def __init__(self, desc, plevel = 0, date = None, due = None, colored = True, tags = []):
        #super(Task, self).__init__()
        self.description = desc
        self.priority = PriorityLevel(plevel, colored)
        self.color = self.priority.color
        self.hash = lambda: self.__hash__()
        def parse(msg):
            # '1d0h30m' -> 1, 0, 30
            # sp = re.compile(r'[ ]{2,}')
            # msg = sp.sub('', msg.strip())
            nd = re.compile(r'\D')
            lst  = nd.split(msg)
            lst = [el for el in lst if el][:3]
            d,h,m = 0,0,0
            out = [d,h,m]
            for idx, el in enumerate(lst):
                out[idx] = int(el)
            return out

        if date:
            try:
                d = dt.strptime(due, "%a %b %d, %Y at %I:%M %p") # parse to dt instance
            except Exception, e:
                print "Unrecognized Date format with value: '%s'." % date
                self.created = Timestamp()
            else:
                self.created = Timestamp(d) # create created
        else:
            self.created = Timestamp()

        if due:
            if 'at' in due:
                try:
                    d = dt.strptime(due, "%a %b %d, %Y at %I:%M %p")
                except Exception, e:
                    print "Unrecognized Date format with value: '%s'." % due
                    self.due = cp.deepcopy(self.created)
                else:
                    self.due =  Timestamp(d)
            else:
                offsets = parse(due)
                self.due = Timestamp(None, *offsets)
        else:
            self.due = cp.deepcopy(self.created)

        self.rep = '%s  %s  Due: %s' % (self.priority, self.description, self.due.hrep)

    def __repr__(self):
        return '<Task: %s>' % self.rep
    def __str__(self):
        return self.rep


class TaskList(object):
    """docstring for TaskList"""
    def __init__(self, tasks = [], labels = []):
        #super(TaskList, self).__init__()
        self.rep = ''
        self.labels = labels
        self.tasks = odict() # {}
        self.repgen = lambda: '\n'.join(['%s' % (self.tasks[t]) for i,t in enumerate(self.tasks)])
        self.set_tasks(tasks)
        self.add = self.__add__
        self.iadd = self.__iadd__
        self.sub = self.__sub__
        self.isub = self.__isub__
        self.remove = self.__isub__
        # should contain the id numbers of all tasks with said label
        # tasks can share labels, not 1:1, but id's should be unique
        self.count = lambda: len(self.tasks)

    def zprint(self, arg = '', rev = False):
        arg = str(arg)
        if arg.strip().upper() == 'CREATED':
            tups = [(self.tasks[k].created.value, self.tasks[k]) for i,k in enumerate(self.tasks)]
        elif arg.strip().upper() == 'PRIORITY':
            tups = [(self.tasks[k].priority.value, self.tasks[k]) for i,k in enumerate(self.tasks)]
        else:
            tups = [(self.tasks[k].due.value, self.tasks[k]) for i,k in enumerate(self.tasks)]
        tups = sorted(tups, key = lambda x: x[0], reverse = rev)
        out = '\n'.join(['%s' % val[1] for val in tups ])
        print out

    def update_state(self):
        self.rep = self.repgen()

    def set_tasks(self, lst):
        [self.tasks.update({t.hash(): t}) for i,t in enumerate(lst)]
        self.update_state()

    def gen_task(self, text, value, due, oldTask = None):
        if type(oldTask) != Task:
            oldtext, oldvalue, olddue, created = [None] * 4
        else:
            t1 = oldTask
            oldtext, oldvalue, olddue, created = [t1.description, t1.priority.value, t1.due.hrep, t1.created.hrep]
        complete = truth(text) and truth(value) and truth(due)
        helptext = '\n'.join(["Using", "\tDescription: %s" % oldtext,
                        "\tLevel: %s" % oldvalue, "\tDue: %s"  % olddue])
        print helptext
        null = ''
        texthelp = ["Enter the new description", "Just write what you need to do."]
        valuehelp = ["Enter the priority level", "Write how hard the task is on a scale of 1-5."]
        duehelp = ["Write in how many days, hours, mins it's due", ""]
        form = FormFiller()
        fn = lambda x: lambda: '%s' % x
        form.addRequiredField('text', str, oldtext, texthelp[0], fn(texthelp[1]) )
        form.addRequiredField('value', int, oldvalue, valuehelp[0], fn(valuehelp[1]) )
        form.addRequiredField('due', str, olddue, duehelp[0], fn(duehelp[1]) )
        vals = form.proccess()
        text, value, due = vals
        out = Task(desc = text, plevel=value, date=created, due=due)
        return out

    def add_task(self, task = None):
        if not task:
            helptext = '\n'.join(["Entering ADD Mode...", "Enter:", "\t'h' or 'help' for help",
            "\t'q' or quit' to exit", "\t'u' or undo' to reset."])
            print helptext
            task =  self.gen_task(None, None, None)
            self.add(task, verbose = True)
        else:
            try:
                self.add(task, verbose = True)
            except Exception, e:
                print e
                task =  self.gen_task(None, None, None)
                self.add(task, verbose = True)
        return task

    def edit_task(self, taskID, updated = None):
        # steps:
        # 0: select ID
        # 1: description (or unchanged)
        # 2: level (or unchanged)
        # 3: due (or unchanged)
        if taskID >= self.count():
            # raise ValueError("Task ID %d out of range(%d)" % (taskID, self.count()) )
            print "Task ID %d out of range(%d)" % (taskID, self.count())
            exit()
        t1 = self.getTask(taskID)
        self.add_task(updated)
        self.remove_task(t1)

    def remove_task(self, taskID):
        self.__del__(taskID, verbose = True)

    def getTask(self, ref):
        if type(ref) == Task:
            h = ref.hash()
            if h in self.tasks:
                return self.tasks[h]
        elif type(ref) == int and ref < self.count():
            h = self.tasks.keys()[ref]
            return self.tasks[h]
        raise(KeyError('Task cannot be found with key: %s' % ref))

    def __sub__(self, task):
        self.__del__(task)

    def __isub__(self, task):
        self.__sub__(task)
        return self

    def __iadd__(self, task):
        self.__add__(task)
        return self

    def __add__(self, task, verbose = False):
        self.tasks.update({task.hash(): task})
        self.update_state()
        if verbose: print 'Succesfully added task\n%s\n' % (task)

    def __radd__(self, task):
        self.__add__(task)

    def __del__(self, reference, verbose = False):
        task = self.getTask(reference)
        self.tasks.pop(task.hash())
        self.update_state()
        if verbose: print 'Succesfully removed task\n%s\n' % (task)

    def __repr__(self):
        return '<TaskList %s>' % self.tasks
    def __str__(self):
        return '%s' % self.rep

if __name__ == '__main__':
    pass
