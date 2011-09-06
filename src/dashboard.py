#!/usr/bin/env python


from PyQt4 import QtGui, QtCore


class Dashboard(QtGui.QFrame):
    
    """
       Class for the dashboard frame which contains all section tabs and their
       applets.
    """
    
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        # Get the QApplication's instance
        self.application = QtCore.QCoreApplication.instance()

        # Set up logger
        self.logger = self.application.logger
        self.logger.info('Logger at Dashboard ready.')

        # Set size according to configuration
        self.setFixedWidth(self.parent().screen_width * 
                           self.application.configuration['ratio'])
        self.setFixedHeight(self.parent().screen_height *
                            self.application.configuration['ratio'])
        self.logger.info('Dashboard size fixed at '+\
                         str(self.maximumWidth())+'*'+\
                         str(self.maximumHeight()))

                         
        self.label = QtGui.QLabel(QtCore.QString('Hiya and hello too!'))

        self.layout = QtGui.QHBoxLayout()

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

