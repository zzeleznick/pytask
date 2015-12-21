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
        usage = "%(prog)s [-h] [-v] [-l | -c | -a | -e | -r] [flags]",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= '')
    parser.add_argument("flags", nargs='?', default = '',
                        help='additonal flags')
    """
    parser.add_argument("keywords", nargs='+', default = ['the'],
                        help='The words to find in the video')
    """
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Adds verbosity')

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-l", "--list", action="store_true",
                        required = False, default = False,
                        help='Shows the TaskList')
    group.add_argument("-c", "--count", action="store_true",
                        required = False, default = False,
                        help='Displays number of active Tasks')
    group.add_argument("-a", "--add", action="store_true",
                        required = False, default = False,
                        help='Adds a task to the TaskList')
    group.add_argument("-e", "--edit", action="store_true",
                        required = False, default = False,
                        help='Edits an existing task')
    group.add_argument("-r", "--remove", action="store_true",
                        required = False, default = False,
                        help='Deletes an existing task')

    args = parser.parse_args()
    # print args
    flags = args.flags
    if flags:
        flags = flags.strip().upper()
    if args.list or flags == 'LIST':
        show()
    elif args.count or flags == 'COUNT':
        print '%d Tasks found' % count()
    elif args.add or flags == 'ADD':
        add()
    elif args.edit or flags == 'EDIT':
        edit()
    elif args.remove or flags == 'REMOVE':
        remove()
    elif flags == 'COUNT' or flags == 'DROP':
        proceed = raw_input("Warning. About to delete all tasks. Enter 'y' to continue\n")
        if proceed.strip().upper() == 'Y':
            print 'Deleting %d tasks ' % count()
            drop()
    elif flags == 'H' or 'HELP' in flags:
        parser.print_help()
    elif not flags:
        show()
    else:
        print "Flag '%s' not found" % flags
    global VERBOSE

    # Handling Options #
    VERBOSE = args.verbose

def get():
    '''
    gets all active tasks
    '''
    ds = build()
    tasksRaw = [line for line in ds.load() if line ]
    tasks = []
    for line in tasksRaw:
        ts, desc, val, dead = line
        tasks += [Task(desc, plevel = val, date = ts, due = dead)]
    lst = TaskList(tasks)
    return lst

def drop():
    '''
    drops all active tasks
    '''
    ds = build()
    ds.dumpTasks()

def write(tasklist):
    ds = build()
    ds.writeTasks(tasklist)

def show():
    '''
    shows all active tasks
    >>> tasker.py list
    '''
    lst = get()
    lst.zprint(arg = 'priority', rev=True)

def count():
    '''
    Counts the number of active tasks
    >>> tasker.py count
    '''
    lst = get()
    return lst.count()

def add():
    '''
    Adds a task
    >>> tasker.py add
    '''
    lst = TaskList() # new instance
    lst.add_task()
    ds = build()
    ds.writeTasks(lst)

def edit():
    '''
    Edits a task
    >>> tasker.py edit
    '''
    lst = get()
    idx = ''
    helptext = '\n'.join(["About to enter EDIT Mode...", "Enter:", "\t'h' or 'help' for help",
            "\t'q' or quit' to exit", "\t'u' or undo' to reset."])
    print helptext
    while idx == '':
        idx = raw_input('Which task would you like to edit:\n')
        if checkHelp(idx):
            print 'Select the (id) of the task that you want to edit'
            idx = ''
            out = '\n'.join(['%s (%d)' % (lst.tasks[t], i) for i,t in enumerate(lst.tasks)])
            print 'All tasks:\n', out
        elif checkExit(idx):
            exit()
        elif checkUndo(idx):
            idx = ''
        if idx:
            try: idx = int(idx)
            except Exception, e: idx = ''
    lst.edit_task(idx)
    drop()
    write(lst)

def remove():
    lst = get()
    idx = raw_input('Which task would you like to delete:\n')
    if idx:
        try: idx = int(idx)
        except Exception, e: idx = ''
    while idx == '':
        out = '\n'.join(['%s (%d)' % (lst.tasks[t], i) for i,t in enumerate(lst.tasks)])
        print 'All tasks:\n', out
        idx = raw_input('Which task would you like to delete:\n')
        cmd = idx.strip().upper()
        if cmd == 'X' or cmd == 'Q' or 'QUIT' in cmd:
            exit()
        if idx:
            try: idx = int(idx)
            except Exception, e: idx = ''
    lst.remove_task(idx)
    drop()
    write(lst)

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