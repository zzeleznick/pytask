#!/usr/bin/env python
# coding=UTF-8
import sys
# from blessings import Terminal
from termcolor import colored # coloring yay
import time
# internals
from classes import *
from utils import *

'''
Program for running todo app
'''

def count():
    '''
    Counts the number of active tasks
    >>> tasker count
    '''
    pass

def edit(idx, args):
    '''
    Edits a task
    '''
    pass

def test():
    t = Timestamp()
    w = PriorityLevel(0)
    desc = 'Finish tasklist'
    t1 = Task(desc)
    t2 = Task(desc, 5)
    t3 = Task(desc, 1)
    t4 = Task(desc, 3)
    t5 = Task(desc, 2)
    print 'TASK 1:', t1
    lst = TaskList([t1, t2, t3])
    print lst, '\n'
    # lst.add(t4)
    # lst += t5
    t4 += lst
    print lst, '\n'
    lst -= t1
    print lst, '\n'
    lst.remove_task(2)
    print lst, '\n'
    lst.edit_task(0)
    print lst

def test2():
    desc = 'Finish tasklist'
    t1 = Task(desc, 2)
    t2 = Task(desc, 5)
    vals = [t1.description, t1.priority.value, t1.timestamp, t1.due]
    writeTask(*vals)
    tasksRaw = loadCurrentTasks()
    tasks = []
    for line in tasksRaw:
        if line:
            print line
            ts, desc, val, dead = line
            tasks += [Task(desc, plevel = val, date = ts, due = dead)]
    lst = TaskList(tasks)
    # print lst
    lst.zprint()
    print '\n'
    lst.zprint(arg = 'priority', rev=True)
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        tasksRaw = loadCurrentTasks()
        tasks = []
        for line in tasksRaw:
            if line:
                ts, desc, val, dead = line
                tasks += [Task(desc, plevel = val, date = ts, due = dead)]
        lst = TaskList(tasks)
        lst.zprint(arg = 'priority', rev=True)
    else:
        print 'booo'