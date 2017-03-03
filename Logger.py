class Logger:

    def __init__(self):
        pass

    @staticmethod
    def info(originator, info_message):
        print "INFO: %s said %s" % (originator.name, info_message,)

    @staticmethod
    def error(originator, error_message):
        print "ERROR: %s launched %s" % (originator.name, error_message,)
