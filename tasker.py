#!/usr/bin/env python
# coding=UTF-8
import sys
import time
import argparse
# libraries
# from blessings import Terminal
from termcolor import colored # coloring yay
# internals
from classes import *
from utils import *
'''
Program for running todo app
'''
def parse_cmd_options():
    parser = argparse.ArgumentParser(
        description="A handy dandy minimal TODO app",
        usage = "%(prog)s [-h] [-v] [-a | -e | -d] [list]",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= '')
    parser.add_argument("list", nargs='+', default = None,
                        help='additonal flags')
    """
    parser.add_argument("keywords", nargs='+', default = ['the'],
                        help='The words to find in the video')
    """
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Adds verbosity')

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-a", "--add", action="store_true",
                        required = False, default = False,
                        help='Adds a task to the TaskList')
    group.add_argument("-e", "--edit", action="store_true",
                        required = False, default = False,
                        help='Edits an existing task')
    group.add_argument("-d", "--delete", action="store_true",
                        required = False, default = False,
                        help='Deletes an existing task')

    args = parser.parse_args()
    print args
    if args.list:
        show()

    global VERBOSE

    # Handling Options #
    VERBOSE = args.verbose

    # return videoName, WORDS, MODE_NAME
def show():
    ds = build()
    tasksRaw = ds.load()
    tasks = []
    for line in tasksRaw:
        if line:
            ts, desc, val, dead = line
            tasks += [Task(desc, plevel = val, date = ts, due = dead)]
    lst = TaskList(tasks)
    lst.zprint(arg = 'priority', rev=True)

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
    ds = build()
    ds.write(*vals)
    tasksRaw = ds.load()
    tasks = []
    for line in tasksRaw:
        if line:
            ts, desc, val, dead = line
            tasks += [Task(desc, plevel = val, date = ts, due = dead)]
    lst = TaskList(tasks)
    # print lst
    lst.zprint()
    print '\n'
    lst.zprint(arg = 'priority', rev=True)

if __name__ == '__main__':
    parse_cmd_options()
    '''
    args = sys.argv[1:]
    if not args:
        ds = build()
        tasksRaw = ds.load()
        tasks = []
        for line in tasksRaw:
            if line:
                ts, desc, val, dead = line
                tasks += [Task(desc, plevel = val, date = ts, due = dead)]
        lst = TaskList(tasks)
        lst.zprint(arg = 'priority', rev=True)
    else:
        test2()
    '''