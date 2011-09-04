#!/usr/bin/env python

from PyQt4 import QtGui, QtCore

import panel


class MainWindow(QtGui.QFrame):
    
    """
        This is a generic class for the main window. It should not be used, but
        its orientated derivates such as MainClassSouth, MainClassNorth etc.
    """

    def __init__(self):
        
        """ Inherits from QFrame. """
        
        # For this QFrame is used and not QWidget, because it offers more
        # flexibility with regard to styling.
                            
        QtGui.QFrame.__init__(self)

        # Get the QApplication's instance
        self.application = QtCore.QCoreApplication.instance()

        # Set up logger
        self.logger = self.application.logger
        self.logger.info('Logger at Main Window ready.')
        
        # Get screen geometry
        self.screen_width = int(QtGui.QDesktopWidget().screenGeometry().width())
        self.screen_height = int(QtGui.QDesktopWidget().screenGeometry().height())
        self.logger.info('Retrieved screen geometry: '+str(self.screen_width)+'*'+\
                                                       str(self.screen_height))

        # Make window transparent
        # Transparency will affect the main widget and all its children.
        # Hence children should be given a style explicitely in the style sheet.
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.logger.info('Tranparency of main window is set.')
        
        # Set all flags required for the WM  to make the application behave 
        # like a dock / panel. It will skip the taskbar, it will have no frame 
        # and stay on top. NB: some of the flags may be redundant.
        self.setWindowFlags(QtCore.Qt.Widget |
            # Always on top:
            QtCore.Qt.WindowStaysOnTopHint |
            # No window decoration
            QtCore.Qt.FramelessWindowHint )
#        # Tell X the window acts as a panel
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)
        self.logger.info('Window flags are set.')


################################################################################
###                         ORIENTATED CLASSES                               ###
################################################################################



class MainWindowSouth(MainWindow):
    
    """
        This main window class holds the geometry settings for southward orientation.    
    """
    
    def __init__(self):
        MainWindow.__init__(self)

        self.logger.info('Initiating South Main Window')

        # set fixed width
        self.setFixedWidth(self.screen_width *
                           self.application.configuration['ratio'])
        self.logger.info('Width of main window set to '+str(self.maximumWidth()))

        # instanciate south-oriented panel
        self.panel = panel.PanelSouth(self)
        self.logger.info('Instanciated South Panel.')
        
        # instanciate vertical layout
        self.layout = QtGui.QVBoxLayout()

        # set stacking order:
        self.layout.setDirection(QtGui.QBoxLayout.TopToBottom) 
        
        # set alignment
        self.layout.setAlignment(QtCore.Qt.AlignBottom)

        # set spacing between widgets in layout
        self.layout.setSpacing(0)

        # set content's margins
        self.layout.setContentsMargins(0, 0, 0, 0)

        # set children
        self.layout.addWidget(self.panel)
        self.logger.info('Panel appended to layout.')
        #TODO: add dash layout

        # set layout
        self.setLayout(self.layout)
        self.logger.info('Layout set.')

        # adjust size to minimum
        self.adjustSize()
        self.logger.info('Size of MainWindow adjusted to: '+\
                         str(self.width())+'*'+str(self.height()))
        
        # define position when hidden
        self.hide_position = QtCore.QPoint((self.screen_width - self.width())/2, # centre horizontally
                                           self.screen_height - self.panel.height()) # height of panel visible only
        self.logger.info('Hide position set to: '+\
                          str(self.hide_position.x())+','+str(self.hide_position.y()))
        
        # define position when shown
        self.show_position = QtCore.QPoint((self.screen_width - self.width())/2, # centre horizontally
                                           self.screen_height - self.height()) # entire window visible
        self.logger.info('Show position set to: '+\
                          str(self.show_position.x())+','+str(self.show_position.y()))

        # move window to hidden position
        self.move(self.hide_position)
        self.logger.info('Moved MainWindow to hide position.')

        # Define space to be reserved by X on the desktop
        # The actual function to reserve space is called in the QApplication
        # after the shoe() method of the main window has been called
        self.reserved_space = (0, 0, 0, self.panel.maximumHeight())



class MainWindowNorth(MainWindow):
    
    """
        This main window class holds the geometry settings for northward orientation.    
    """
    
    def __init__(self):
        MainWindow.__init__(self)
        
        self.logger.info('Initiating North Main Window')

        # set fixed width
        self.setFixedWidth(self.screen_width *
                           self.application.configuration['ratio'])
        self.logger.info('Width of main window set to '+str(self.maximumWidth()))

        # instanciate north-oriented panel
        self.panel = panel.PanelNorth(self)
        self.logger.info('Instanciated North Panel.')
        
        # instanciate vertical layout
        self.layout = QtGui.QVBoxLayout()

        # set stacking order:
        self.layout.setDirection(QtGui.QBoxLayout.BottomToTop)

        # set alignment
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        # set spacing between widgets in layout
        self.layout.setSpacing(0)

        # set content's margins
        self.layout.setContentsMargins(0, 0, 0, 0)

        # set children
        self.layout.addWidget(self.panel)
        self.logger.info('Panel appended to layout.')
        #TODO: add dash layout

        # set layout
        self.setLayout(self.layout)
        self.logger.info('Layout set.')

        # adjust size to minimum
        self.adjustSize()
        self.logger.info('Size of MainWindow adjusted to: '+\
                         str(self.width())+'*'+str(self.height()))
        
        # define position when hidden
        # FIXME: may need to change is hiding dashboard while moved up because then self.height() will change.
        self.hide_position = QtCore.QPoint((self.screen_width - self.width())/2, # centre horizontally
                                           self.panel.height() - self.height()) # height of panel visible only
        self.logger.info('Hide position set to: '+\
                          str(self.hide_position.x())+','+str(self.hide_position.y()))
        
        # define position when shown
        self.show_position = QtCore.QPoint((self.screen_width - self.width())/2, # centre horizontally
                                            0) # entire window visible
        self.logger.info('Show position set to: '+\
                          str(self.show_position.x())+','+str(self.show_position.y()))

        # move window to hidden position
        self.move(self.hide_position)
        self.logger.info('Moved MainWindow to hide position.')

        # Define space to be reserved by X on the desktop
        # The actual function to reserve space is called in the QApplication
        # after the shoe() method of the main window has been called
        self.reserved_space = (0, 0, self.panel.maximumHeight(), 0)


class MainWindowWest(MainWindow):
    
    """
        This main window class holds the geometry settings for westward orientation.    
    """
    
    def __init__(self):
        MainWindow.__init__(self)

        self.logger.info('Initiating North Main Window')

        # set fixed height
        self.setFixedHeight(self.screen_height *
                           self.application.configuration['ratio'])
        self.logger.info('Height of main window set to '+str(self.maximumHeight()))

        # instanciate north-oriented panel
        self.panel = panel.PanelWest(self)
        self.logger.info('Instanciated West Panel.')
        
        # instanciate vertical layout
        self.layout = QtGui.QHBoxLayout()

        # set stacking order:
        self.layout.setDirection(QtGui.QBoxLayout.RightToLeft)

        # set alignment
        self.layout.setAlignment(QtCore.Qt.AlignLeft)

        # set spacing between widgets in layout
        self.layout.setSpacing(0)

        # set content's margins
        self.layout.setContentsMargins(0, 0, 0, 0)

        # set children
        self.layout.addWidget(self.panel)
        self.logger.info('Panel appended to layout.')
        #TODO: add dash layout

        # set layout
        self.setLayout(self.layout)
        self.logger.info('Layout set.')

        # adjust size to minimum
        self.adjustSize()
        
        # define position when hidden
        self.hide_position = QtCore.QPoint(self.panel.width() - self.width(), # width of panel visible only
                                           (self.screen_height - self.height())/2) # centered vertically
        self.logger.info('Hide position set to: '+\
                          str(self.hide_position.x())+','+str(self.hide_position.y()))

        # define position when shown
        self.show_position = QtCore.QPoint(0, # entire window visible
                                            (self.screen_height - self.height())/2) # centered vertically
        self.logger.info('Show position set to: '+\
                          str(self.show_position.x())+','+str(self.show_position.y()))

        # move window to hidden position
        self.move(self.hide_position)
        self.logger.info('Moved MainWindow to hide position.')

        # Define space to be reserved by X on the desktop
        # The actual function to reserve space is called in the QApplication
        # after the shoe() method of the main window has been called
        self.reserved_space = (self.panel.maximumWidth(), 0, 0, 0)


class MainWindowEast(MainWindow):
    
    """
        This main window class holds the geometry settings for eastward orientation.    
    """
    
    def __init__(self):
        MainWindow.__init__(self)

        self.logger.info('Initiating North Main Window')

        # set fixed height
        self.setFixedHeight(self.screen_height *
                           self.application.configuration['ratio'])
        self.logger.info('Height of main window set to '+str(self.maximumHeight()))

        # instanciate north-oriented panel
        self.panel = panel.PanelEast(self)
        
        # instanciate vertical layout
        self.layout = QtGui.QHBoxLayout()

        # set stacking order:
        self.layout.setDirection(QtGui.QBoxLayout.LeftToRight)

        # set alignment
        self.layout.setAlignment(QtCore.Qt.AlignRight)

        # set spacing between widgets in layout
        self.layout.setSpacing(0)

        # set content's margins
        self.layout.setContentsMargins(0, 0, 0, 0)

        # set children
        self.layout.addWidget(self.panel)
        self.logger.info('Panel appended to layout.')
        #TODO: add dash layout

        # set layout
        self.setLayout(self.layout)
        self.logger.info('Layout set.')

        # adjust size to minimum
        self.adjustSize()
        
        # define position when hidden
        self.hide_position = QtCore.QPoint(self.screen_width - self.panel.width(), # width of panel visible only
                                           (self.screen_height - self.height())/2) # centered vertically
        self.logger.info('Hide position set to: '+\
                          str(self.hide_position.x())+','+str(self.hide_position.y()))

        # define position when shown
        self.show_position = QtCore.QPoint(self.screen_width - self.width(), # entire window visible
                                            (self.screen_height - self.height())/2) # centered vertically
        self.logger.info('Show position set to: '+\
                          str(self.show_position.x())+','+str(self.show_position.y()))

        # move window to hidden position
        self.move(self.hide_position)
        self.logger.info('Moved MainWindow to hide position.')

        # Define space to be reserved by X on the desktop
        # The actual function to reserve space is called in the QApplication
        # after the shoe() method of the main window has been called
        self.reserved_space = (0, self.panel.maximumWidth(), 0, 0)


    
