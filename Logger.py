class Logger:

    def __init__(self):
        pass

    @staticmethod
    def info(originator, info_message):
        print "INFO: %s said %s" % (originator.name, info_message,)

    @staticmethod
    def error(originator, error_message):
        print "ERROR: %s launched %s" % (originator.name, error_message,)

    @staticmethod
    def log_it(function):
        def wrapper(*passed_args):
            try:
                originator = passed_args[0].__class__.__name__
                action = function.__name__
                arg_names = function.func_code.co_varnames[:function.func_code.co_argcount]
                args = passed_args[:len(arg_names)]
                print "INFO: %s starting to %s" % (originator, action,)
                result = function(*args)
                print "INFO: %s finished doing %s" % (originator, action,)
                return result
            except Exception, e:
                print "ERROR: %s launched %s" % (originator, e.message,)

        return wrapper

