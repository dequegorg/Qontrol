#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

__version__ = "11.09.06.14.38"

################################################################################
###                           PANEL CLASS                                    ###
################################################################################

class Panel(QtGui.QFrame):

    """
        Class of the main transparent frame circumscribing the panel bar and dock.
        It is invisible and used for structural purpose only.     
    """

    def __init__(self, orientation):
        QtGui.QFrame.__init__(self)
        
        # Reference QApplication
        self.application = QtCore.QCoreApplication.instance()

        # Get logger
        self.logger = self.application.logger

        # Reference orientation
        self.orientation = orientation
        self.logger.info('Panel orientation is '+self.orientation)

        # Get screen geometry
        self.screen_width = int(QtGui.QDesktopWidget().screenGeometry().width())
        self.screen_height = int(QtGui.QDesktopWidget().screenGeometry().height())
        self.logger.info('Screen geometry is '+ \
                          str(self.screen_width)+'*'+ \
                          str(self.screen_height))

        # Make layout
        self.layout = self.make_layout()
        
        # Define bar orientation option
        # NB: specific subclass should be used for style reference regarding orientation
        self.bar_orientation_options = {'south' : BarSouth,
                                        'north' : BarNorth,
                                        'west' : BarWest,
                                        'east' : BarEast}

        # Add children (before geometry because position depends on children size)
        self.bar = self.bar_orientation_options[self.orientation](self, self.orientation)
        self.layout.addWidget(self.bar)
        
        # Fix layout        
        self.setLayout(self.layout)
        
        # Set geometry
        self.set_geometry()
        
        # Set appearance
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # Set behaviour on X
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)

        # Set reserved space
        self.set_reserved_space()


    def set_reserved_space(self):
        
        """
           Define space to be reserved by X on the desktop.
           The actual function to reserve space is called in the QApplication
           after the show() method of the main window has been called
        """
        
        if self.orientation == 'south':
            self.reserved_space = (0, 0, 0, self.bar.maximumHeight())
        elif self.orientation == 'north':
            self.reserved_space = (0, 0, self.bar.maximumHeight(), 0)
        elif self.orientation == 'west':
            self.reserved_space = (self.bar.maximumWidth(), 0, 0, 0)
        elif self.orientation == 'east':
            self.reserved_space = (0, self.bar.maximumWidth(), 0, 0)
        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()
            

    def set_geometry(self):
        
        """
            Organises and sets geometry of the panel's main frame according to
            orientation.
            NB: Do not confuse with Qt's QWidget.setGeometry() !
        """
        
        # Fix height or width depending on orientation 
        if self.orientation in ('north', 'south'):
            # Horizontal
            self.setFixedWidth(self.screen_width)
            self.logger.info('Width of panel fixed at '+ \
                             str(self.maximumWidth()))
        
        elif self.orientation in ('west', 'east'):
            # Vertical
            self.setFixedHeight(self.screen_height)
            self.logger.info('Height of panel fixed at '+ \
                             str(self.maximumHeight()))
        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        # Reduce size to minimum necessary        
        self.adjustSize()
        self.logger.info('Size of Panel adjusted to: '+\
                         str(self.width())+'*'+str(self.height()))


        # Find out where to anchor the panel
        # On X axis         
        if self.orientation in ('north', 'west', 'south'):
            pos_x = 0

        elif self.orientation in ('east'):
            pos_x = self.screen_width - self.bar.maximumWidth()

        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()
        
        # on Y axis
        if self.orientation in ('north', 'west', 'east'):
            pos_y = 0

        if self.orientation in ('south'):
            pos_y = self.screen_height - self.bar.maximumHeight()

        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()
        
        self.anchor_position = QtCore.QPoint(pos_x, pos_y)
        self.logger.info('Anchor for Panel set at '+ \
                         str(self.anchor_position))
        self.move(self.anchor_position)

       
        
    def make_layout(self):
        
        """
            Composes layout according to orientation.        
        """
        
        # Find out whether layout's verical or horizontal
        if self.orientation in ('north', 'south'):
            # vertical
            layout = QtGui.QVBoxLayout()
            self.logger.info('Panel layout set vertically.')
        elif self.orientation in ('west', 'east'):
            # horizontal
            layout = QtGui.QHBoxLayout()
            self.logger.info('Panel layout set horizontally.')
        else:
            # we're in trouble -- quit
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        # Set staking order and alignment
        if self.orientation == 'south':
            layout.setDirection(QtGui.QBoxLayout.BottomToTop)
            layout.setAlignment(QtCore.Qt.AlignBottom)

        elif self.orientation == 'north':
            layout.setDirection(QtGui.QBoxLayout.TopToBottom)
            layout.setAlignment(QtCore.Qt.AlignTop)

        elif self.orientation == 'west':
            layout.setDirection(QtGui.QBoxLayout.LeftToRight)
            layout.setAlignment(QtCore.Qt.AlignLeft)

        elif self.orientation == 'east':
            layout.setDirection(QtGui.QBoxLayout.RightToLeft)
            layout.setAlignment(QtCore.Qt.AlignRight)

        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        # Arrange margins and padding:
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        return layout



################################################################################
###                          BAR META CLASS                                  ###
################################################################################

class Bar(QtGui.QFrame):

    """
        The Bar is set on the edge-most side of the Panel.
        It holds buttons to switch the dashboard.
    """
    
    def __init__(self, parent, orientation):
        
        """
            Inherits from QFrame.     
        """
        
        # Originally, the panel inherited from QToolBar, but QToolbar does not
        # support the border-image style property
        # (cf. http://doc.trolltech.com/4.6/stylesheet-reference.html#border-image-prop)

        QtGui.QFrame.__init__(self, parent)

        # Reference QApplication
        self.application = QtCore.QCoreApplication.instance()

        # Get logger
        self.logger = self.application.logger

        # Reference orientation
        self.orientation = orientation
        self.logger.info('Bar orientation is '+self.orientation)

        # Make layout:
        self.layout = self.make_layout()
        self.setLayout(self.layout)
        
        # Make buttons:
        self.make_buttons()

        # Set geometry:
        self.set_geometry()


    def make_layout(self):
        
        """
            Composes Bar layout according to orientation.        
        """
        
        # Find out whether layout's verical or horizontal
        if self.orientation in ('north', 'south'):
            # horizontal
            layout = QtGui.QHBoxLayout()
            self.logger.info('Bar layout set horizontally.')
        elif self.orientation in ('west', 'east'):
            # horizontal
            layout = QtGui.QVBoxLayout()
            self.logger.info('Bar layout set vertically.')
        else:
            # we're in trouble -- quit
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        # Set button alignment
        alignment_options = {'left' : QtCore.Qt.AlignLeft,
                             'right' : QtCore.Qt.AlignRight,
                             'top'  : QtCore.Qt.AlignTop,
                             'bottom' : QtCore.Qt.AlignBottom,
                             'center' : QtCore.Qt.AlignCenter
                            }
        alignment = self.application.configuration['panel']['button-alignment']
        # Check if requested alignment is coherent with orientation
        if alignment in ('left', 'right') and self.orientation in ('west', 'east'):
            # not coherent
            self.logger.warn('Button alignment is not coherent with orientation.')
            alignment = center
        if alignment in ('top', 'bottom') and self.orientation in ('north', 'east'):
            # not coherent
            self.logger.warn('Button alignment is not coherent with orientation.')
            alignment = center
        # Alignment now coherent
        layout.setAlignment(alignment_options[alignment])

        # Arrange margins and padding:
        layout.setSpacing(self.application.configuration['panel']['button-spacing'])
        layout.setContentsMargins(self.application.configuration['panel']['margin-vertical'], # Left
                                  self.application.configuration['panel']['margin-horizontal'], # Top
                                  self.application.configuration['panel']['margin-vertical'], # Right
                                  self.application.configuration['panel']['margin-horizontal'],) # Bottom

        return layout



    def set_geometry(self):
        
        """
            Organises and sets geometry of the Bar according to
            orientation.
            NB: Do not confuse with Qt's QWidget.setGeometry() !
        """
        
        # Fix height or width depending on orientation and configuration
        if self.orientation in ('north', 'south'):
            # Horizontal
            self.setFixedWidth(self.parent().screen_width)
            self.logger.info('Width of Bar fixed at '+ \
                             str(self.maximumWidth()))
            self.setFixedHeight(self.application.configuration['panel']['thickness'])
            self.logger.info('Height of Bar fixed at '+ \
                             str(self.maximumHeight()))
        elif self.orientation in ('west', 'east'):
            # Vertical
            self.setFixedHeight(self.parent().screen_height)
            self.logger.info('Height of Bar fixed at '+ \
                             str(self.maximumHeight()))
            self.setFixedWidth(self.application.configuration['panel']['thickness'])
            self.logger.info('Width of Bar fixed at '+ \
                             str(self.maximumWidth()))
        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        

    def make_buttons(self):
        
        """
            Fetch buttons from a list in configuration.
            Each button is connected to a page of the dashboard to switch its
            content and show/hide the dashboard altogether.
            Buttons are also indicators, notifying the user of activity on the
            dashboard when hidden.
        """
            
        # TODO: Get the indicators configuration file:
        
        # TODO: Get a list of all indicators

        # TODO: Check which indicators are enabled

        # TODO: Import and append indicators to the panel

        switch_one = QtGui.QPushButton('switch one', self)
        self.connect(switch_one, QtCore.SIGNAL('clicked()'),
                            self.application.dashboard.check_position)
        self.layout.addWidget(switch_one)

            

################################################################################
###                           BAR ORIENTED CLASSES                           ###
################################################################################

# Oriented classes all derive from the Bar Class and should not inherit from one
# another in order for to keep their respective style separate in the style sheet

class BarSouth(Bar):
      
    """
        Bar sub-class for southward orientation.    
    """

    def __init__(self, parent, orientation):
        Bar.__init__(self, parent, orientation)


class BarNorth(Bar):
      
    """
        Bar sub-class for northward orientation.    
    """

    def __init__(self, parent, orientation):
        Bar.__init__(self, parent, orientation)


class BarWest(Bar):
      
    """
        Bar sub-class for westward orientation.    
    """

    def __init__(self, parent, orientation):
        Bar.__init__(self, parent, orientation)

class BarEast(Bar):
      
    """
        Bar sub-class for eastward orientation.    
    """

    def __init__(self, parent, orientation):
        Bar.__init__(self, parent, orientation)
