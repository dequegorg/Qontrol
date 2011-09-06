#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

class Panel(QtGui.QFrame):
    
    def __init__(self, parent):
        
        """
            Inherits from QFrame.     
        """
        
        # Originally, the panel inherited from QToolBar, but QToolbar does not
        # support the border-image style property
        # (cf. http://doc.trolltech.com/4.6/stylesheet-reference.html#border-image-prop)

        QtGui.QFrame.__init__(self, parent)
        

    def fetch_indicators(self):
        
        """
            Fetch indicators from a list of enabled indicators in a confifugration
            file.
        """
            
        # TODO: Get the indicators configuration file:
        
        # TODO: Get a list of all indicators

        # TODO: Check which indicators are enabled

        # TODO: Import and append indicators to the panel

        pass

################################################################################
###                           ORIENTED CLASSES                               ###
################################################################################

# Oriented classes all derive from Panel and should not inherit from one another
# in order for to keep their respective style separate in the style sheet

class PanelSouth(Panel):
      
    """
        This Panel class holds the geometry settings for southward orientation.    
    """

    def __init__(self, parent):
        Panel.__init__(self, parent)

        self.setFixedHeight(25)
        self.setFixedWidth(self.parent().maximumWidth())


class PanelNorth(Panel):
      
    """
        This Panel class holds the geometry settings for northward orientation.    
    """

    def __init__(self, parent):
        Panel.__init__(self, parent)

        self.setFixedHeight(25)
        self.setFixedWidth(self.parent().maximumWidth())


class PanelWest(Panel):
      
    """
        This Panel class holds the geometry settings for westward orientation.    
    """

    def __init__(self, parent):
        Panel.__init__(self, parent)

        self.setFixedHeight(self.parent().maximumWidth())
        self.setFixedWidth(25)

class PanelEast(Panel):
      
    """
        This Panel class holds the geometry settings for southward orientation.    
    """

    def __init__(self, parent):
        Panel.__init__(self, parent)

        self.setFixedHeight(self.parent().maximumWidth())
        self.setFixedWidth(25)
