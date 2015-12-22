from tasker import *
from classes import *
from utils import build

def test_build():
    build()

def test_Priority():
    for i in range(7):
        print i, 'colored:', PriorityLevel(i)
        print i, 'base:', PriorityLevel(i, colored = False)

def test_Timestamp():
    for d,h,m in zip(range(5),range(5),range(5)):
        print d, Timestamp(None, d, h, m)
        print d, Timestamp(None, d, h, m).as24hour()

def test_Form(basic = False, user_input = False):
    form = FormFiller()
    fn = lambda x: lambda: 'Put %s up all in me!' % x
    var1, var2, var3 = ["name", "value", "date"]
    form.addRequiredField(var1, str, 'poop', '', fn(var1) )
    form.addRequiredField(var2, int, 3, '', fn(var2) )
    form.addRequiredField(var3)
    print form
    if user_input:
        vals = form.proccess()
    else:
        form.setField(var1, 'Zach')
        form.setField(var3, Timestamp())
        if not basic:
            try:
                form.setField(var2, 'Bad input')
            except Exception, e:
                print(e)
                form.setField(var2, 2)
        vals = form.fields.values()
    print form
    print 'Values: %s' % vals

def test_Construction():
    print '----Constructing 3 tasks-----'
    desc = 'Build tasklist'
    t1 = Task(desc)
    t2 = Task(desc, 5)
    t3 = Task(desc, 1)
    out = ['%d: %s' % (i, t) for i,t in enumerate([t1,t2,t3])]
    print '\n'.join(out)
    print '----End Constructing 3 tasks-----'
    print '----Constructing 3-item TaskList-----'
    lst = TaskList([t1, t2, t3])
    print 'Result\n', lst
    print '----End Constructing 3-item TaskList-----'

def test_Add_Subtract():
    print '----Constructing 3 tasks-----'
    desc = 'Test adding tasklist'
    t1 = Task(desc, 1)
    t2 = Task(desc, 2)
    t3 = Task(desc, 3)
    out = ['%d: %s' % (i, t) for i,t in enumerate([t1,t2,t3])]
    print '\n'.join(out)
    print '----End Constructing 3 tasks-----'
    print '----Constructing 0-item TaskList-----'
    lst = TaskList()
    print 'Result\n', lst
    print '----End Constructing 0-item TaskList-----'
    print '----Adding 3 Tasks-----'
    lst += t1
    (lst.iadd(t2)).add(t3)
    print 'Result\n', lst
    print '----End Adding 3 Tasks-----'
    print '----Removing 1st, 3rd Tasks-----'
    lst - t3
    lst.remove_task(0)
    print 'Result\n', lst
    print '----End Removing 1st, 3rd Tasks-----'

def test_Edit(user_input = False):
    print '----Constructing 2 tasks-----'
    desc = 'Test edit_task'
    t1 = Task(desc, 1)
    t2 = Task(desc, 2)
    out = ['%d: %s' % (i, t) for i,t in enumerate([t1,t2])]
    print '\n'.join(out)
    print '----End Constructing 2 tasks-----'
    print '----Adding 2 Tasks-----'
    lst = TaskList()
    (lst.iadd(t1)).add(t2)
    print 'Result\n', lst
    print '----End Adding 2 Tasks-----'
    if user_input:
        print '----Editing id(0) task-----'
        lst.edit_task(0)
        print 'Result\n', lst
        print '----End Editing id(0) task-----'

def test_IO():
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
    lst.zprint()
    print '\n'
    lst.zprint(arg = 'priority', rev=True)

if __name__ == '__main__':
    test_Add_Subtract()