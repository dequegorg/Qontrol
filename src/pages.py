#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

__version__ = "11.09.06.14.38"



class Page(QtGui.QFrame):

    """
        Page populating the QStackedLayout of the dashboard, it can contain
        widgets. It owns an indicator that is placed on the panel's bar.    
    """

    def __init__(self, parent, name):
        QtGui.QFrame.__init__(self, parent)

        # Get the QApplication's instance
        self.application = QtCore.QCoreApplication.instance()

        # Set up logger
        self.logger = self.application.logger
        self.logger.info('Logger at '+name+' ready.')

        # Set Geometry
#        self.setFixedSize(self.parent().maximumWidth(), 
#                                self.parent().maximumHeight())
#        self.logger.info('Size of page '+name+' set to:'+ \
#                          str(self.maximumWidth())+'*'+str(self.maximumHeight()))
        
        # TODO: Indicator will need its own class for styling reference
        self.indicator = QtGui.QPushButton(name+' Indicator')

#################################################################################
####                          PAGE ORIENTED CLASS                             ###
#################################################################################


#class PageSouth(Page):
#    
#    """
#        Subclass of Page oriented southwards.
#    """
#    def __init__(self, parent, name):
#        Page.__init__(self, parent, name)

#class PageNorth(Page):
#    
#    """
#        Subclass of Page oriented northwards.
#    """
#    def __init__(self, parent, name):
#        Page.__init__(self, parent, name)

#class PageWest(Page):
#    
#    """
#        Subclass of Page oriented westwards.
#    """
#    def __init__(self, parent, name):
#        Page.__init__(self, parent, name)

#class PageEast(Page):
#    
#    """
#        Subclass of Page oriented southwards.
#    """
#    def __init__(self, parent, name):
#        Page.__init__(self, parent, name)


################################################################################
###                          DUMMY PAGE FOR TESTING                          ###
################################################################################


class DummyPage(Page):

    """
        Dummy page used for testing dashboard.    
    """
    
    def __init__(self, parent, name):
        Page.__init__(self, parent, name)

        self.logger.info('Parent of '+name+' is '+str(self.parent()))

        self.label = QtGui.QLabel(QtCore.QString('<h1>'+name.upper()+'</h1>'), self)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

