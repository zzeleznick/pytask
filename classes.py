import sys
import time
import copy as cp
import re

from termcolor import colored # coloring yay
from datetime import datetime as dt
# internals
from utils import *

EPOCH = dt.fromtimestamp(0)
colors = ["blue", "green", "yellow", "red"]
levels = ["Default", "Easy", "Medium", "Hard"]
edges =  [0, 2, 3, 5]
mycolor = lambda x: colors[sorted(edges + [x]).index(x)]
mylevel = lambda x: levels[sorted(edges + [x]).index(x)]

class PriorityLevel(object):
    """docstring for PriorityLevel"""
    def __init__(self, val):
        # super(PriorityLevel, self).__init__()
        # input value can 0-5,
        # { 0: [0, blue, unset], 1: [1-2, green, easy],
        # 2: [3, yellow, med],  3: [4-5: red, hard]}
        high = 5
        if type(val) != int:
            try: val = int(val)
            except Exception, e: val = 0
        val = min(max(val, 0), high)
        self.value = (val) % (high+1)
        self.color = mycolor(self.value)
        self.level = mylevel(self.value)
        self.rep = '%s %d' % (self.level, self.value)
        self.hrep = '*' * (self.value) + ' ' * (high - self.value)
    def __repr__(self):
        return '<Label: %s>' % self.rep
    def __str__(self):
        return colored(self.hrep, self.color) # self.hrep

class Timestamp(object):
    """docstring for Timestamp"""
    def __init__(self, date = None, d_offset = 0, h_offset = 0, m_offset = 0):
        # super(Timestamp, self).__init__()
        if not date:
            t = dt.now() # current date
        else:
            t = date
        self.value = int((t - EPOCH).total_seconds()) # seconds since epoch
        offset = (((d_offset * 24 + h_offset) * 60) + m_offset)  * 60
        if offset:
            self.value += offset
        self.date = dt.fromtimestamp(self.value) # date object
        self.rep = dt.strftime(self.date, "%Y-%m-%d %H:%M:%S") # timestamp
        self.hrep = dt.strftime(self.date, "%a %b %d, %Y at %I:%M %p") # human readable timestamp
    def asDate(self):
        return self.date
    def __repr__(self):
        return '<TS %s>' % self.rep
    def __str__(self):
        return self.hrep


class TaskList(object):
    """docstring for TaskList"""
    def __init__(self, tasks = [], labels = []):
        #super(TaskList, self).__init__()
        self.rep = ''
        self.labels = labels
        self.tasks = {}
        self.repgen = lambda: '\n'.join(['%s' % (self.tasks[t]) for i,t in enumerate(self.tasks)])
        self.set_tasks(tasks)
        self.add = self.__add__
        self.remove = self.__sub__
        # should contain the id numbers of all tasks with said label
        # tasks can share labels, not 1:1, but id's should be unique
        self.count = lambda: len(self.tasks)

    def zprint(self, arg = '', rev = False):
        if arg.strip().upper() == 'CREATED':
            tups = [(self.tasks[k].timestamp.value, self.tasks[k]) for i,k in enumerate(self.tasks)]
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
        # [self.tasks.update({i: t}) for i,t in enumerate(lst)]
        [self.tasks.update({t.hash(): t}) for i,t in enumerate(lst)]
        self.update_state()
    def gen_task(self, desc, level, due, oldTask = None):
        if type(oldTask) != Task:
            vals = [None] * 4
        else:
            t1 = oldTask
            vals = [t1.description, t1.priority.value, t1.due.hrep, t1.timestamp.hrep]
        complete = truth(desc) and truth(level) and truth(due)
        helptext = '\n'.join(["Using", "\tDescription: %s" % vals[0],
                        "\tLevel: %s" % vals[1], "\tDue: %s"  % vals[2]])
        print helptext
        while not complete:
            complete = truth(desc) and truth(level) and truth(due)
            if not desc or not desc.strip():
                desc = raw_input('Enter the new description:\n')
                if checkHelp(desc):
                    print 'Write what you need to do!'
                    continue
                elif checkExit(desc):
                    exit()
                elif checkUndo(desc):
                    due = ''
                    continue
                if not truth(desc):
                    desc = vals[0]
            if not level:
                level = raw_input('Enter the priority level:\n')
                if checkHelp(level):
                    print 'Write how hard the task is on a scale of 1-5.'
                    continue
                elif checkExit(level):
                    exit()
                elif checkUndo(level):
                    desc = ''
                    continue
                try: level = int(level)
                except Exception, e: level = vals[1]
            if not due:
                due = raw_input("Enter in how many days-hours-mins it's due:\n")
                if checkHelp(due):
                    print "Write how many days-hours-mins it's due"
                    continue
                elif checkExit(due):
                    exit()
                elif checkUndo(due):
                    level = 0
                    continue
                if not truth(due):
                    due = vals[2]
        out = Task(desc = desc, plevel=level, date= vals[3], due=due)
        return out

    def add_task(self, text = '', val = 0, due = ''):
        complete = truth(text) and truth(val) and truth(due)
        if not complete:
            helptext = '\n'.join(["Entering ADD Mode...", "Enter:", "\t'h' or 'help' for help",
            "\t'q' or quit' to exit", "\t'u' or undo' to reset."])
            print helptext
            t2 =  self.gen_task(text, val, due)
        else:
            try:
                t2 = self.gen_task(text, val, due)
            except Exception, e:
                print e
                t2 =  self.gen_task(None, None, None)
        self + t2
        return t2
    def edit_task(self, taskID, desc = None, level = 0, due = None):
        # steps:
        # 0: select ID
        # 1: description (or unchanged)
        # 2: level (or unchanged)
        # 3: due (or unchanged)
        if taskID >= self.count():
            # raise ValueError("Task ID %d out of range(%d)" % (taskID, self.count()) )
            print "Task ID %d out of range(%d)" % (taskID, self.count())
            exit()
        complete = truth(desc) and truth(level) and truth(due)
        h = self.tasks.keys()[taskID]
        t1 = self.tasks[h]
        if not complete:
            helptext = '\n'.join(["Entering EDIT Mode...", "Enter:", "\t'h' or 'help' for help",
            "\t'q' or quit' to exit", "\t'u' or undo' to reset."])
            print helptext
            t2 =  self.gen_task(desc, level, due, oldTask = t1)
        else:
            try:
                t2 =  self.gen_task(desc, level, due, oldTask = t1)
            except Exception, e:
                print e
                t2 =  self.gen_task(None, None, None, oldTask = t1)
        self.tasks[h] = t2
        print 'Succesfully updated task\nOLD: %s\nNEW: %s' % (t1, t2)
        self.update_state()
    def remove_task(self, taskID):
        if taskID < self.count():
            self.__del__(taskID)
    def __sub__(self, task):
        if type(task) == Task:
            if task.hash() in self.tasks:
                self.tasks.pop(task.hash())
                self.update_state()
        elif type(task) == int:
            self.remove_task(task)
    def __add__(self, task):
        self.tasks.update({self.count()+1: task})
        print 'Succesfully added task\n%s\n' % (task)
        self.update_state()
    def __radd__(self, task):
        self.__add__(task)
    def __iadd__(self, task):
        self.__add__(task)
        return self
    def __isub__(self, task):
        self.__sub__(task)
        return self
    def __del__(self, taskID):
        h = self.tasks.keys()[taskID]
        task = self.tasks[h]
        self.tasks.pop(h)
        print 'Succesfully removed task\n%s\n' % (task)
        self.update_state()
    def __repr__(self):
        return '<TaskList %s>' % self.tasks
    def __str__(self):
        return '%s' % self.rep

class Task(object):
    """docstring for Task"""
    def __init__(self, desc, plevel = 0, date = None, due = None, tags = []):
        #super(Task, self).__init__()
        self.description = desc
        self.priority = PriorityLevel(plevel)
        self.color = self.priority.color
        self.hash = lambda: self.__hash__()
        def parse(msg):
            # '1d0h30m' -> 1, 0, 30
            nd = re.compile(r'\D')
            lst  = nd.split(msg.strip())
            d,h,m,idx = 0,0,0,0
            out = [d,h,m]
            possible = [el for idx, el in enumerate(lst) if el and idx < len(out)]
            for el in possible:
                try:
                    val = int(el)
                except Exception, e:
                    pass
                else:
                    out[idx] = val
                    idx += 1
            return out

        if not date:
            self.timestamp = Timestamp()
        else:
            d = dt.strptime(date, "%a %b %d, %Y at %I:%M %p")
            self.timestamp = Timestamp(d)
        if not due:
            self.due = cp.deepcopy(self.timestamp)
        else:
            if 'at' in due:
                d = dt.strptime(date, "%a %b %d, %Y at %I:%M %p")
                self.due =  Timestamp(d)
            else:
                offsets = parse(due)
                self.due = Timestamp(None, *offsets)
        self.rep = '%s  %s  Due: %s' % (self.priority, self.description, self.due.hrep)
    def __repr__(self):
        return '<Task: %s>' % self.rep
    def __str__(self):
        return colored(self.rep, self.color)

'''
class TaskList(object):
    """docstring for TaskList"""
    __tasks = {} # shared class variable
    __labels = []

    @staticmethod
    def countTasks():
        return len(TaskList.__tasks)
'''