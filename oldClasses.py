from generics import Command

class FormFiller(object):
    """
    INFO: Class for getting values of required fields w/ types
    USAGE:
        - form = FormFiller()
        - form.addRequiredField(<args>)
        - values = form.proccess()
    """
    def __init__(self, null = ''):
        self.null = null
        self.incomplete = self.checkForMissingValues
        self.counter = 0
        self.fields = odict()
        self.defaults = odict()
        self.help = odict()
        self.count = lambda: len(self.fields)

    def checkForMissingValues(self):
        for key in self.fields:
            if self.fields[key] == self.null:
                return True
        return False

    def setField(self, name, value, soft_exit = False):
        convert = self.defaults[name][0]
        try:
            parsed = convert(value)
        except Exception, e:
            if soft_exit: print e
            else: raise(e)
        else:
            self.fields[name] = parsed
            self.counter += 1

    def addRequiredField(self, name, expected = str, default = '', helptext = '', helpfnc = lambda: ''):
        if not default:
            default = self.null
        if not helptext:
            helptext = "Enter %s for '%s'." % (type(default), name)
        self.fields[name] = self.null
        self.defaults[name] = (expected, default)
        self.help[name] = (helptext, helpfnc)

    def runHelpFnc(self, idx):
        key = self.fields.keys()[idx]
        return self.help[key][1]()

    def getPrompt(self, idx):
        key = self.fields.keys()[idx]
        return self.help[key][0]

    def requestInput(self, idx):
        print self.getPrompt(idx)

    def consumeInput(self):
        """
        INFO: Main Method to walk users through filling out all required fields.
        NOTES:
            - if user input maps to exit, exits
            - if user input maps to help, displays help
            - if user input maps to undo, resets last input
        """
        raw = raw_input()
        idx = self.counter
        key = self.fields.keys()[idx]
        cmd = Command(raw)
        if cmd.is_exit():
            print 'exit triggered'
            exit()
        elif cmd.is_help():
            print self.runHelpFnc(idx)
        elif cmd.is_undo():
            self.counter = max(0, self.counter - 1)
            key = self.fields.keys()[self.counter]
            self.fields[key] = self.null
        elif not raw:
            cached = self.defaults[key][1]
            if cached:
                self.setField(key, cached, soft_exit = True)
        else:
            self.setField(key, raw, soft_exit = True)

    def proccess(self):
        while self.incomplete():
            # print 'Counter at', self.counter
            self.requestInput(self.counter)
            self.consumeInput()
        return self.fields.values()

    def __repr__(self):
        return '<Form with fields %s>' % self.fields.keys()

    def __str__(self):
        head = '--Begin Form--'
        end = '--End Form--'
        fields = ["'%s': %s" % (name, val) for name, val in self.fields.items()]
        print self.defaults.values()
        defaults = ["%s, default: '%s'" % (exp, val) for exp, val in self.defaults.values()]
        pairs = zip(fields, defaults)
        lines = [', '.join(pair) for pair in pairs]
        return '\n'.join([head, '\n'.join(lines), end])

"""
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
"""