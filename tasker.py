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
        description="Dynamically creates a supercut from a video and subtitle pairing\nwhere the keyword(s) of interest are spoken",
        usage = "%(prog)s [-h] [-v] [-p | -w | -s] [videoName] [keywords]",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= listVideoFiles() )

    parser.add_argument("filename",  metavar= 'video', nargs='?', default = None,
                        help='The video to process')
    parser.add_argument("keywords", nargs='+', default = ['the'],
                        help='The words to find in the video')
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Displays the phrases that contain the keyword(s) if True')

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-p", "--phrase", action="store_true",
                        required = False, default = False,
                        help='Captures the entire phrase')
    group.add_argument("-w", "--word", action="store_true",
                        required = False, default = False,
                        help='Refines the bounds to include just the word')
    group.add_argument("-s", "--speech", action="store_true",
                        required = False, default = False,
                        help='Creates a fake speech from the keywords')

    args = parser.parse_args()
    print args

    global VERBOSE
    global WORDS
    global MODE_NAME

    videoName = args.filename
    WORDS  = args.keywords
    options = [args.phrase, args.word, args.speech]

    # Check if input arguments are valid #
    valid = testUserInput(videoName)
    if not valid:
        print 'Try a video file from the list [%s] ' % listVideoFiles()
        exit()
    # End input validation #

    # Handling Options #
    VERBOSE = args.verbose

    if True in options:
        MODE = options.index(True)
    else:
        MODE = 0

    optionNames = ['phrases', 'words', 'speech']
    MODE_NAME = optionNames[MODE]

    print "Finding the words: %s\nVideo Name: %s\nOption: %s" % (WORDS, videoName, MODE_NAME)
    # End Handling Options #

    return videoName, WORDS, MODE_NAME
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