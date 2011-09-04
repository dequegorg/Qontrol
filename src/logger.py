#!/usr/bin/env python

from time import strftime, localtime
from os import path
import inspect

class Logger(object):
    
    """
        Logger class to print input to log file and to console if verbose is on.
    """
    
    def __init__(self, log_path, verbose=False):
        self.verbose = verbose
        self.message_types = {'info' : 92,
                              'warning' : 33,
                              'error' : 91,
                              'log error': 95}

        file_name = strftime('%y%m%d%H%M%S', localtime())+'.log'
        self.file_name = path.expanduser(path.join(log_path, file_name))
        self.info('Logger initiated.')
        object.__init__(self)
        
    def info(self, message):
        self.log(message, 'info')

    def warn(self, message):
        self.log(message, 'warning')

    def error(self, message):
        self.log(message, 'error')
   

    def log(self, message, message_type):
        
        # list of items to print:
        elements = []

        # make time-stamp        
        time_stamp = strftime('%y.%m.%d.%H.%M.%S ', localtime())
        elements.append(time_stamp)

        # make frame-stamp
        current_frame = inspect.currentframe()
        call_frame = inspect.getouterframes(current_frame, 1)
        frame = call_frame[2]
        call_file = frame[1].split('/')[-1].ljust(15)
        call_line = str('%04d' % int(frame[2]))
        frame_stamp = '@File: '+call_file+' @Line: '+call_line+': '
        elements.append(frame_stamp)

        # fromat message type:
        elements.append(message_type.upper().center(8))        
        
        # check if there is a message content:
        if message == None:
            message = "LOG MESSAGE OMITTED!"
            message_type = 'log error'
        # fromat message to string
        message = str(message)
        elements.append(message)

        # compose string:
        string = ' '.join(elements)+'\n'
        
        # open file to write to:
        try:
            log_file = open(self.file_name, 'a')
            log_file.write(string)
            log_file.close()
        except:
            raise
        
        # print to screen if required
        if self.verbose == True:
            print elements[0]+' '+elements[1]+\
            ' \033[1m\033[%dm'%self.message_types[message_type]+\
            elements[2]+'\033[0m '+elements[3]
        

def test_logger():
    print "A test is run for logger:"
    logger = Logger('~/Desktop', True)
    logger.info('test info')
    logger.warn('test warning')
    logger.error('test error')
    logger.info('')
    

if __name__ == "__main__":
    
    test_logger()
    

