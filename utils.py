import re
from datetime import datetime as dt
import csv
# internals
from config import buildConfig

EPOCH = dt.fromtimestamp(0)
colors = ["blue", "green", "yellow", "red"]
levels = ["Default", "Easy", "Medium", "Hard"]
edges =  [0, 2, 3, 5]
mycolor = lambda x: colors[sorted(edges + [x]).index(x)]
mylevel = lambda x: levels[sorted(edges + [x]).index(x)]

def build(zvals = []):
    ds = buildConfig(zvals)
    return ds.getVals()

def loadCurrentTasks(fname = None, buildArr = []):
    if not fname:
        DATA_FOLDER, CURRENT_TASKS, COMPLETED_TASKS, DELETED_TASKS = build(buildArr)
        fname = DATA_FOLDER + CURRENT_TASKS
    with open(fname, 'rb') as infile:
        reader = csv.reader(infile, delimiter='@')
        out = [row for row in reader] # list of list of strings
    return out

def writeTask(desc, plevel, created, due, fname = None, buildArr = []):
    if not fname:
        DATA_FOLDER, CURRENT_TASKS, COMPLETED_TASKS, DELETED_TASKS = build(buildArr)
        fname = DATA_FOLDER + CURRENT_TASKS
    with open(fname, 'a') as csvfile:
      zwriter = csv.writer(csvfile, delimiter='@',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
      zwriter.writerow([created] + [desc] + [plevel] + [due])

def test0():
    arr1 = ['derp/', '1.csv', '2.csv', '3.csv']
    test(arr1)

def test(arr = []):
    DATA_FOLDER, CURRENT_TASKS, COMPLETED_TASKS, DELETED_TASKS = build(arr)
    tasks = loadCurrentTasks(fname = None, buildArr = arr)
    # if type(tasks[0]) == list:
    o1 = '\n'.join([' '.join([c for c in row]) for row in tasks])
    print 'Original File:\n', o1
    writeTask('test', '1', 'now', 'later', fname = None, buildArr = arr)
    tasks = loadCurrentTasks(fname = None, buildArr = arr)
    o2 = '\n'.join([' '.join([c for c in row]) for row in tasks])
    print 'Post File:\n', o2

def parseDue(msg):
    # '1d0h30m' -> 1, 0, 30
    nd = re.compile(r'\D')
    lst  = nd.split(msg.strip())
    d,h,m = 0,0,0
    out = [d,h,m]
    idx = 0
    for el in lst:
        if idx >= len(out): break
        if el:
            try: val = int(el)
            except Exception, e: pass
            else:
                out[idx] = val
                idx += 1
    return out

if __name__ == '__main__':
    # test()
    # test0()
    pass