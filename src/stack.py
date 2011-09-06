#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

import pages

__version__ = "11.09.06.14.38"



################################################################################
###                       STACK META CLASS                                   ###
################################################################################


class Stack(QtGui.QFrame):
     
    """
        Frame with stacked layout for the dashboard, holding pages.    
    """

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

                # Get the QApplication's instance
        self.application = QtCore.QCoreApplication.instance()

        # Set up logger
        self.logger = self.application.logger
        self.logger.info('Logger at Stack ready.')

        # Reference orientation
        self.orientation = self.parent().orientation
        self.logger.info('Stack has orientation '+self.orientation)

        # Set Geometry
        self.setFixedSize(self.parent().maximumWidth(), 
                          self.parent().maximumHeight())
        self.logger.info('Size of stack set to:'+ \
                          str(self.maximumWidth())+'*'+str(self.maximumHeight()))

        # Set layout
        self.layout = QtGui.QStackedLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setContentsMargins(20, 20, 20, 0)
        
        # Set pages
        for name in self.application.configuration['dashboard']['pages']:
            page = pages.DummyPage(self, name)

            self.layout.addWidget(page)
        
        self.setLayout(self.layout)

        count = self.layout.count()
        self.logger.info(str(count)+" pages were appended to dashboard stack.")

            

################################################################################
###                          STACK ORIENTED CLASSES                          ###
################################################################################


class StackSouth(Stack):
    
    """
        Subclass of Stack oriented southwards.
    """
    def __init__(self, parent):
        Stack.__init__(self, parent)

class StackNorth(Stack):
    
    """
        Subclass of Stack oriented northwards.
    """
    def __init__(self, parent):
        Stack.__init__(self, parent)

class StackWest(Stack):
    
    """
        Subclass of Stack oriented westwards.
    """
    def __init__(self, parent):
        Stack.__init__(self, parent)

class StackEast(Stack):
    
    """
        Subclass of Stack oriented eastwards.
    """
    def __init__(self, parent):
        Stack.__init__(self, parent)
