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
from config import buildConfig

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
            try:
                found_count = count()
            except Exception, e:
                print(e)
                proceed = raw_input("Continue? Enter 'y' to proceed.\n")
                if proceed.strip().upper() == 'Y': drop()
            else:
                print 'Deleting %d tasks ' % found_count
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

def build(zvals = []):
    '''
    The locations of the various data files
    Folder location, and filenames if customized
    default = [ 'data/', 'CURRENT.csv', 'COMPLETED.csv', 'DELETED.csv']
    '''
    return buildConfig(zvals)

def get(colored = True):
    '''
    gets all active tasks
    '''
    ds = build()
    tasksRaw = [line for line in ds.load() if line ]
    tasks = []
    for line in tasksRaw:
        ts, desc, val, dead = line
        tasks += [Task(desc, value = val, date = ts, due = dead, colored = colored)]
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

def getTaskID(action, tasklist):
    ''' returns the index of the task via User Input'''
    action = (str(action)).strip()
    info = "About to enter %s Mode...\nEnter:\n" % (action.upper())
    helpkeys = "\t'h' or 'help' for help"
    undokeys = "\t'u' or undo' to reset."
    esckeys = "\t'q' or quit' to exit"
    helptext = '\n'.join([info, helpkeys, undokeys, esckeys])
    print helptext
    null = ''
    idx = null
    idxh1 = 'Select the (id) of the task that you want to %s' % action
    idxh2 = '\n'.join(['%s (%d)' % (tasklist.tasks[t], i) for i,t in enumerate(tasklist.tasks)])
    idxhelp = '\n'.join(["All tasks:", idxh1, idxh2])
    while idx == null:
        idx = raw_input('Which task would you like to %s \n' % action)
        if checkExit(idx):
            exit()
        idx = handleHelp(idx, idxhelp, null)
        if checkUndo(idx):
            idx = null
        if idx:
            try: idx = int(idx)
            except Exception, e: idx = null
    return idx

def edit():
    '''
    Edits a task
    >>> tasker.py edit
    '''
    lst = get()
    idx = getTaskID('edit', lst)
    lst.edit_task(idx)
    drop()
    # print lst
    write(lst)

def remove():
    '''
    Removes a task
    >>> tasker.py remove
    '''
    lst = get()
    idx = getTaskID('delete', lst)
    lst.remove_task(idx)
    drop()
    write(lst)

if __name__ == '__main__':
    parse_cmd_options()