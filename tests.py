from tasker import *
from classes import *
from utils import build

def test():
    t = Timestamp()
    w = PriorityLevel(0)
    desc = 'Finish tasklist'
    t1 = Task(desc)
    t2 = Task(desc, 5)
    t3 = Task(desc, 1)
    t4 = Task(desc, 3)
    t5 = Task(desc, 2)
    # print 'TASK 1:', t1
    print '----Constructing 3 tasks-----'
    lst = TaskList([t1, t2, t3])
    print '-----3 TASKS----\n', lst, '\n-----END 3 TASKS----'
    print '----Adding 4th task-----'
    t4 += lst
    print '-----4 TASKS----\n', lst, '\n-----END 4 TASKS----'
    print '----Removing 1st task-----'
    lst -= t1
    print '-----3 TASKS----\n', lst, '\n-----END 3 TASKS----'
    print '----Removing id(2) task-----'
    lst.remove_task(2)
    print '-----2 TASKS----\n', lst, '\n-----END 2 TASKS----'
    # print '----Editing id(0) task-----'
    # lst.edit_task(0)
    # print '-----2 TASKS----\n', lst, '\n-----END 2 TASKS----'
    lst.add(t5)
    print '-----3 TASKS----\n', lst, '\n-----END 3 TASKS----'

def test2():
    desc = 'Finish tasklist'
    t1 = Task(desc, 2)
    t2 = Task(desc, 5)
    vals = [t1.description, t1.priority.value, t1.created, t1.due]
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
    test()