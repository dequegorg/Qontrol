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

        # Define sections of the dashboard to switch to like tabs
        self.sections = ['Applications',
                         'Documents',
                         'System',
                         'Communications',
                         'World',
                         'News',
                         'Organiser',
                         'Sound',
                         'Video']

        # create layout:
        self.layout = QtGui.QVBoxLayout()
        
        # add tabs
        self.tabs = Tabs(self, self.sections)
        self.layout.addWidget(self.tabs)
      
        # set layout
        self.setLayout(self.layout)
            




class Tabs(QtGui.QTabWidget):
    
    # TODO: Perhaps use QStackedLayout instead?
    
    """
        Class for content area of the dashboard.    
    """
    
    def __init__(self, parent, sections):
        QtGui.QTabWidget.__init__(self, parent)

        self.setTabPosition(QtGui.QTabWidget.South)
        self.tabBar().setExpanding(True)

        for section in sections:
            # TODO: replace content by actual content
            label = QtCore.QString(section)
            content = QtGui.QLabel(label)
            self.addTab(content, label)

#class Content(QtGui.QWidget):

#    """
#        Widget representing content of dashboard.
#    """

#    def __init__(self, label):
#        QtGui.QWidget.__init__(self)

#        self.label = 

