import sys
import time
import copy as cp

from termcolor import colored # coloring yay
from datetime import datetime as dt
# internals
from utils import *

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
    def edit_task(self, taskID, priority = 0, desc = None):
        if taskID >= self.count():
            raise ValueError("Task ID %d out of range(%d)" % (taskID, self.count()) )
        if not desc:
            desc = raw_input('Enter the new description:\n')
        if not priority:
            plevel = raw_input('Enter the priority level:\n')
            try:
                plevel = int(plevel)
            except Exception, e:
                plevel = 0
        h = self.tasks.keys()[taskID]
        self.tasks[h] = Task(desc, plevel)
        self.update_state()
    def remove_task(self, taskID):
        if taskID < self.count():
            h = self.tasks.keys()[taskID]
            task = self.tasks[h]
            self.tasks.pop(h)
            self.update_state()
    def __sub__(self, task):
        if type(task) == Task:
            if task.hash() in self.tasks:
                self.tasks.pop(task.hash())
                self.update_state()
        elif type(task) == int:
            self.remove_task(task)
    def __add__(self, task):
        self.tasks.update({self.count()+1: task})
        self.update_state()
    def __radd__(self, task):
        self.__add__(task)
    def __iadd__(self, task):
        self.__add__(task)
        return self
    def __isub__(self, task):
        self.__sub__(task)
        return self
    def __repr__(self):
        return '<TaskList %s>' % self.tasks
    def __str__(self):
        return '%s' % self.rep

'''
class TaskList(object):
    """docstring for TaskList"""
    __tasks = {} # shared class variable
    __labels = []

    @staticmethod
    def countTasks():
        return len(TaskList.__tasks)
'''

class Task(object):
    """docstring for Task"""
    def __init__(self, desc, plevel = 0, date = None, due = None, tags = []):
        #super(Task, self).__init__()
        self.description = desc
        self.priority = PriorityLevel(plevel)
        self.color = self.priority.color
        self.hash = lambda: self.__hash__()
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
                offsets = parseDue(due)
                self.due = Timestamp(None, *offsets)
        self.rep = '%s  %s  Due: %s' % (self.priority, self.description, self.due.hrep)
    def __repr__(self):
        return '<Task: %s>' % self.rep
    def __str__(self):
        return colored(self.rep, self.color)
