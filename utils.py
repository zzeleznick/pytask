# useful functions

iterReq = lambda d, x: "Arg '%s' of %s must be iterable." % (d, type(x))
sameLengthReq = lambda x, y: 'Fields (%d) and Types (%d) must have same length.' % (len(x), len(y))
CMD = lambda x: x.strip().upper()
checkHelp = lambda x: 1 if (CMD(x) == 'H' or CMD(x) == 'HELP') else 0
checkExit = lambda x: 1 if (CMD(x) == 'X' or CMD(x) == 'Q' or CMD(x) == 'QUIT') else 0
checkUndo =  lambda x: 1 if (CMD(x) == 'B' or CMD(x) == 'U' or CMD(x) == 'UNDO') else 0

def handleHelp(x, msg, null):
    if checkHelp(x):
        print msg
        return null
    else:
        return x
