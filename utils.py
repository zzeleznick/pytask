from datetime import datetime as dt
import re
# internals
from config import buildConfig

truth = lambda x: True if x else False
CMD = lambda x: x.strip().upper()
checkHelp = lambda x: 1 if (CMD(x) == 'H' or CMD(x) == 'HELP') else 0
checkExit = lambda x: exit() if (CMD(x) == 'X' or CMD(x) == 'Q' or CMD(x) == 'QUIT') else lambda: 0
checkUndo =  lambda x: 1 if (CMD(x) == 'B' or CMD(x) == 'U' or CMD(x) == 'UNDO') else 0

def handleHelp(val, msg, nulled = ''):
    if checkHelp(val):
        print msg
        return nulled
    else:
        return val

def handleUndo(val, prior, nulled = ''):
    return nulled if checkUndo(val) else prior

def build(zvals = []):
    ds = buildConfig(zvals)
    return ds

if __name__ == '__main__':
    pass