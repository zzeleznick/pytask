from datetime import datetime as dt
import re
# internals
from config import buildConfig

def build(zvals = []):
    ds = buildConfig(zvals)
    return ds

def test0():
    arr1 = ['derp/', '1.csv', '2.csv', '3.csv']
    test(arr1)

def test(arr = []):
    ds = build(arr)
    tasks = ds.load()
    o1 = '\n'.join([' '.join([c for c in row]) for row in tasks])
    print 'Original File:\n', o1
    ds.write('test', '1', 'now', 'later')
    tasks = ds.load()
    o2 = '\n'.join([' '.join([c for c in row]) for row in tasks])
    print 'Post File:\n', o2

if __name__ == '__main__':
    # test()
    # test0()
    pass