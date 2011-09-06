#!/usr/bin/env python


__author__="benjamin"
__version__ = '11.09.06.14.37'



################################################################################
#                                IMPORTS                                       #
################################################################################

import sys
import os
import json # used to get and set configuration file
from PyQt4 import QtGui, QtCore

import xwindow # module used to grab window on X for reserving space
from logger import Logger

import panel
import dashboard

################################################################################
#                             MAIN APPLICATION                                 #
################################################################################


class Application(QtGui.QApplication):
    
    """
       Main application class derived from QApplication.
       Few things are appended to this class:
            * the path to the user directory
            * a logger to monitor runtime
            * a style sheet for appearance 
    """
    
    def __init__(self):
        QtGui.QApplication.__init__(self, sys.argv)
        
        # enumerate path to user home and subdirectories        
        self.directories = {
                    'main'  :   os.path.expanduser('~/.qontrol'),
                    'log'   :   os.path.expanduser('~/.qontrol/log'),
                    'cnf'   :   os.path.expanduser('~/.qontrol/cnf'),
                    'thm'   :   os.path.expanduser('~/.qontrol/thm'),
                    'ind'   :   os.path.expanduser('~/.qontrol/ind')
                                }
        
        # get verbose option for logger        
        self.verbose = True if 'verbose' in sys.argv else False        
        
        # create logger and pass in the verbose option
        try:
            self.logger = Logger(self.directories['log'], self.verbose)
        except IOError as error:
            if error[0] == 2:
                # in that case the path does not exist and it should be created
                # with make_directories
                self.make_directories()
                try:
                    # try making the logger again
                    self.logger = Logger(self.directories['log'], self.verbose)
                except:
                    raise                
            else:
                raise error
        
        # define default configuration
        self.default_configuration = {
                                      'style' : 'default',
                                      'language' : 'english',
                                      'orientation' : 'south',
                                      'dashboard' : {'ratio' : 0.8},
                                      'panel' : {'margin-vertical' : 2,
                                                 'margin-horizontal' : 2,
                                                 'button-spacing' : 2,
                                                 'button-alignment' : 'center',
                                                 'thickness' : 25}
                                      }
        
        # get user configuration
        self.logger.info('Fetching user configuration.')
        self.configuration = self.get_config()

        # set QT style from style sheet
        try:
            self.setStyleSheet(QtCore.QString(self.get_style()))
            self.logger.info('Style is set.')
        except Exception as error:
            self.logger.error('There was a problem while applying style: '+\
                               error.strerror+' Running without style.')
            # the stylsheet string may be damaged, run without style
            pass
        
        # Instantiate windows from class befitting orientation in configuration
        # If error in configuration, southward orientation becomes default
        self.dashboard = dashboard.Dashboard(self.configuration['orientation'])
        self.dashboard.show()
        self.panel = panel.Panel(self.configuration['orientation'])
        self.panel.show()
        self.logger.info('Request was made to paint the Dashboard and Panel.')
        
        # Grab window instance from X for reserving space.
        # This can only be done here, after show() has been called.        
        self.x_window = xwindow.Window(self.panel.winId())
        self.x_window.reserve_space(*self.panel.reserved_space)
        self.logger.info('Reserved space for window was requested from X.')
        

    
    def make_directories(self):
        
        """
            This method will create directories in the user's path if those do
            not already exist.   
        """

        # check if directories exist and if not, make them:
        for key, directory in self.directories.iteritems():
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as error:
                    pass


    def get_style(self):

        """
            This method will try to get a custom style from the user directory.
            If it fails, it will use the default style instead.
        """
        
        # check which style is requested in configuration
        try:
            style_name = self.configuration['style']
            self.logger.info('Requested style is "'+style_name+'".')
        except Exception as error:
            # there is something wrong with the configuration it must be reset
            self.logger.warn('There was a problem with the configuration: '+error.strerror)
            self.configuration = self.get_config()
            self.logger.info('Reverting to default style.')
            style_name = 'default'
        
        # look for the style in the user path
        try:
            self.logger.info('Trying to open style from user directory.')
            style_address = os.path.join(self.directories['thm'], style_name)
            style_file = open(style_address, 'r')
        except Exception as error:
            self.logger.warn('There was a problem opening style sheet: '+error.strerror)
            # the file is not to be found in the user's path or
            # the directory does not exist
            # make sure directory exists:
            self.make_directories()
        
            # look for the style in the current root path
            try:
                self.logger.info('Trying to open style from root directory.')
                style_address = os.path.join(os.path.dirname(__file__), 'thm', style_name)
                style_file = open(style_address, 'r')
            except Exception as error:
                self.logger.warn('There was a problem loading the stylesheet: '+error.strerror)
                # the file does not exist
                # revert to default style and try again if it wasn't so
                if style_name != 'default':
                    self.logger.info('Reverting to default style.')
                    style_name = 'default'
                    # look for the style in the current root path
                    try:
                        style_address = os.path.join(os.path.dirname(__file__), 'thm', style_name)
                        style_file = open(style_address, 'r')
                    except Exception as error:
                        self.logger.warn('There was a problem loading default style: '+\
                            error.strerror+' Running without style instead')
                        # then there is no style found, run without style
                        return ''
                else:
                    self.logger.warn('There was a problem loading default style. '+\
                        error.strerror+' Running without style instead')
                    # then there is no style found, run without style
                    return ''
            
        # try to read the style file obtained
        try:        
            style = style_file.read()
        except Exception as error:
            self.logger.warn('There was a problem reading the stylesheet: '+error.strerror)
            # the style file was unreadable
            # try default style if it wasn't so
            if style_name != 'default':
                self.logger.info('Reverting to default style.')
                style_name = 'default'
                # look for the style in the current root path
                try:
                    style_address = os.path.join(os.path.dirname(__file__), 'thm', style_name)
                    style_file = open(style_address, 'r')
                except Exception as error:
                    self.logger.warn('There was a problem loading default style: '+\
                        error.strerror+' Running without style instead.')
                # then there is no style file found, run without style
                    return ''
                # try to read default if found                
                try:
                    style = style_file.read()
                except Exception as error:
                    self.logger.warn('There was a problem reading default style. '+\
                        error.strerror+' Running without style instead.')
                    # the default style was unreadable, run without style
                    style_file.close()
                    return ''
            else:
                self.logger.warn('There was a problem reading default style. '+\
                        error.strerror+' Running without style instead')
                # the default style was already in request and unreadable, run without style
                return ''
            
        # try to close file
        try:
            style_file.close()
        except Exception as error:
            self.logger.warn('There was a problem closing the stylesheet: '+error.strerror)
            # could not close the file, but no big deal
            pass 
            
        # return style to main application
        return style


    def get_config(self):
        
        """
            This method will try to get the user configuration.
            If it fails, it will make reset the configuration.
        """
        
        # define address of user configuration        
        address = os.path.join(self.directories['cnf'], 'user.cnf')
        # try to open it        
        try:
            self.logger.info('Fetching configuration file at: '+address)
            configuration_file = open(address, 'r')
        except IOError as error:
            if error[0] == 2:
                self.logger.warn('The configuration file or its path may not exist.')
                # in that case the path or file do not exist
                # and it should be created with make_directories
                self.make_directories()
                try:
                    # try getting the configuration again
                    configuration_file = open(address, 'r')
                except IOError as error:
                    if error[0] == 2:
                        self.logger.info('The configuration file does not exist.')
                        # in that case the configuration file does not exist
                        # it must be created from scratch              
                        return self.set_config()
                    else:
                    # something else went wrong
                        self.logger.error('There was an error loading the configuration file: '+ \
                                         error.strerror)
            else:
            # something else went wrong
                self.logger.error('There was an error loading the configuration file: '+ \
                                    error.strerror)
        
        # we can proceed with loading the configuration
        try:
            configuration = json.loads(configuration_file.read())
        except Exception as error:
            self.logger.warn('There was a problem reading the configuration file: '+ \
                             error.strerror)
            # there was a problem reading the configuration file
            # it will be reset to default
            return self.set_config()
        # if all is well:
        return configuration


    def set_config(self):

        """
            This method will create a config file from scratches,
            and return it to the application.
        """
        
        # define address for user configuration file        
        address = os.path.join(self.directories['cnf'], 'user.cnf')
        self.logger.info('A new configuration file will be created at '+address)
        
        # try to open it        
        try:
            configuration_file = open(address, 'w')
        except IOError as error:
            if error[0] == 2:
                self.logger.info('The path of the address is missing.')
                # in that case the path does not exist
                # and it should be created with make_directories
                self.make_directories()
                try:
                    # try getting the configuration again
                    configuration_file = open(address, 'w')
                except Exception as error:
                    # something else went wrong
                    self.logger.error('There was a problem creating a configuration file: '+ \
                                        error.strerror)
            else:
                # something else went wrong
                self.logger.error('There was a problem creating a configuration file'+ \
                                   error.strerror)
        except Exception as error:
                # something else went wrong
                self.logger.error('There was a problem creating a configuration file: '+ \
                                    error.strerror)
        
        # try to write to file
        try:
            configuration_file.write(json.dumps(self.default_configuration))
        except Exception as error:
            # something went wrong
            self.logger.error('There was a problem writing to the configuration file: '+ \
                               error.strerror)
        
        # try to close:
        try:
            configuration_file.close()
        except Exception as error:
            # something went wrong
            self.logger.warn('There was a problem closing the configuration file: '+ \
                              error.strerror)
        
        # return default configuration to the main application:
        return self.default_configuration

   


if __name__ == "__main__":
    # create global variable for logger
    application = Application()
    sys.exit(application.exec_())
