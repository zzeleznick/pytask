import os
'''
#example config
DATA_FOLDER = 'data/'
CURRENT_TASKS = 'CURRENT.csv'
COMPLETED_TASKS = 'COMPLETED.csv'
DELETED_TASKS = 'DELETED.csv'
'''
# editable
# VARS = ['DATA_FOLDER', 'CURRENT_TASKS', 'COMPLETED_TASKS', 'DELETED_TASKS']
# end editable
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
    def build(self, vals):
        if vals and type(vals) == list and len(vals) >= 4:
            VALS = vals
        else:
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

def buildConfig(zvals = []):
    return DataStore(zvals)
