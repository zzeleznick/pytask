# file for creating config
import os
import csv

class DataStore(object):
    """docstring for PriorityLevel"""
    def __init__(self, vals):
        zvals = self.build(vals)
        self.DATA_FOLDER = zvals[0]
        self.CURRENT_TASKS = zvals[1]
        self.COMPLETED_TASKS = zvals[2]
        self.DELETED_TASKS = zvals[3]
        self.getVals = lambda: [self.DATA_FOLDER, self.CURRENT_TASKS,
                                self.COMPLETED_TASKS, self.DELETED_TASKS]
        self.load = self.loadCurrentTasks
        self.write = self.writeTask
    def build(self, vals):
        if vals and type(vals) == list and len(vals) >= 4:
            VALS = vals
        else:
            favorite = '/Users/zeleznick/tasker/'
            try:
                os.chdir(favorite)
            except Exception, e:
                pass
            VALS = [ 'data/', 'CURRENT.csv',
                    'COMPLETED.csv', 'DELETED.csv']
        if not os.path.isdir(VALS[0]):
            print 'DATA_FOLDER %s not on path. Creating now...' % VALS[0]
            os.mkdir(VALS[0])
        for name in VALS[1:]:
            if name not in os.listdir(VALS[0]):
                f = open(VALS[0] + name, 'w')
                f.close()
        return VALS

    def loadCurrentTasks(self):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'rb') as infile:
            reader = csv.reader(infile, delimiter='@')
            out = [row for row in reader] # list of list of strings
        return out

    def dumpTasks(self):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        f = open(fname, 'w')
        f.close()

    def writeTasks(self, taskList):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'a') as csvfile:
            zwriter = csv.writer(csvfile, delimiter='@',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for idx, key in enumerate(taskList.tasks):
                t1 = taskList.tasks[key]
                desc, value = [t1.description, t1.priority.value]
                due, created = [t1.due.hrep, t1.created.hrep]
                zwriter.writerow([created] + [desc] + [value] + [due])

    def writeTask(self, desc, value, created, due):
        fname = self.DATA_FOLDER + self.CURRENT_TASKS
        with open(fname, 'a') as csvfile:
            zwriter = csv.writer(csvfile, delimiter='@',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            zwriter.writerow([created] + [desc] + [value] + [due])

    def __repr__(self):
        return '<DS %s | %s>' % (self.DATA_FOLDER, self.CURRENT_TASKS)
    def __str__(self):
        return repr(self)

def buildConfig(zvals = []):
    ds = DataStore(zvals)
    return ds

if __name__ == '__main__':
    pass