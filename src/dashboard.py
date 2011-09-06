#!/usr/bin/env python


from PyQt4 import QtGui, QtCore

__version__ = "11.09.06.14.38"


################################################################################
###                         DASHBOARD META CLASS                             ###
################################################################################

class Dashboard(QtGui.QFrame):
    
    """
       Class for the dashboard frame with stacked layout, which shows / hides.
    """
    
    def __init__(self, orientation):
        QtGui.QFrame.__init__(self)

        # Get the QApplication's instance
        self.application = QtCore.QCoreApplication.instance()

        # Set up logger
        self.logger = self.application.logger
        self.logger.info('Logger at Dashboard ready.')

        # Reference orientation
        self.orientation = orientation

        # Get screen geometry
        self.screen_width = int(QtGui.QDesktopWidget().screenGeometry().width())
        self.screen_height = int(QtGui.QDesktopWidget().screenGeometry().height())

        # Set size according to configuration
        self.setFixedWidth(self.screen_width * 
                           self.application.configuration['dashboard']['ratio'])
        self.setFixedHeight(self.screen_height *
                            self.application.configuration['dashboard']['ratio'])

        self.logger.info('Dashboard size fixed at '+\
                         str(self.maximumWidth())+'*'+\
                         str(self.maximumHeight()))

        # Set position
        self.define_positions()
        self.move(self.show_position)

        # DUMMY CONTENT
        self.label = QtGui.QLabel(QtCore.QString('<h1>DASHBOARD</h1>'))
        self.layout = QtGui.QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Tell X the window acts as a panel
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)
    

    def define_positions(self):

        """
            Defines show and hide position according to orientation.
        """
        
        # Define show_position on X axis
        if self.orientation in ('north', 'south'):
            pos_x = (self.screen_width - self.maximumWidth())/2
        elif self.orientation in ('west'):
            pos_x = self.application.configuration['panel']['thickness']
        elif self.orientation in ('east'):
            pos_x = self.screen_width - self.maximumWidth() - \
                    self.application.configuration['panel']['thickness']
        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()
         
        # Define show_position on Y axis
        if self.orientation in ('west', 'east'):
            pos_y = (self.screen_height - self.maximumHeight())/2
        elif self.orientation in ('north'):
            pos_y = self.application.configuration['panel']['thickness']
        elif self.orientation in ('south'):
            pos_y = self.screen_height - self.maximumHeight() - \
                    self.application.configuration['panel']['thickness']
        else:
            # This shouldn't happen, but we never know
            self.logger.error("I need a proper layout :( ")
            QtCore.QCoreApplication.quit()

        self.show_position = QtCore.QPoint(pos_x, pos_y)
        self.logger.info('Dashboard show position set to '+\
                        str(self.show_position.x())+', '+\
                        str(self.show_position.y()))

        # Define hide_position on X axis
        if self.orientation in ('west'):
            pos_x = - self.maximumWidth()
        elif self.orientation in ('east'):
            pos_x = self.screen_width + self.maximumWidth()
        else:
            # North and South don't need change on X axis
            pass
        
        # Define show_position on Y axis
        if self.orientation in ('north'):
            pos_y = - self.maximumHeight()
        elif self.orientation in ('south'):
            pos_y = self.screen_height + self.maximumHeight()
        else:
            # West and East don't need change on Y axis
            pass

        self.hide_position = QtCore.QPoint(pos_x, pos_y)
        self.logger.info('Dashboard hide position set to '+\
                        str(self.hide_position.x())+', '+\
                        str(self.hide_position.y()))


    def check_position(self):

        """
            Calls for animation after checking current position.        
        """

        if self.pos() == self.show_position:
            self.hide_dashboard()

        if self.pos() == self.hide_position:
            self.show_dashboard()



    def show_dashboard(self):
        
        """
            Triggers animation that will show the entire dashboard.
        """

        self.show_animation = QtCore.QPropertyAnimation(self, "pos")
        self.show_animation.setDuration(200)
        self.show_animation.setStartValue(self.hide_position)
        self.show_animation.setEndValue(self.show_position)
        self.show_animation.start()



    def hide_dashboard(self):
        
        """
            Triggers animation that will hide the entire dashboard.
        """

        self.hide_animation = QtCore.QPropertyAnimation(self, "pos")
        self.hide_animation.setDuration(200)
        self.hide_animation.setStartValue(self.show_position)
        self.hide_animation.setEndValue(self.hide_position)
        self.hide_animation.start()    

################################################################################
###                   DASHBOARD ORIENTATED CLASES                            ###
################################################################################


# used to determine orientation in styles

class DashboardSouth(Dashboard):

    """
        Dashboard sub-class dor southward orientation.
    """

    def __init__(self, orientation):
        Dashboard.__init__(self, orientation)

class DashboardNorth(Dashboard):

    """
        Dashboard sub-class dor northward orientation.
    """

    def __init__(self, orientation):
        Dashboard.__init__(self, orientation)


class DashboardWest(Dashboard):

    """
        Dashboard sub-class dor westward orientation.
    """

    def __init__(self, orientation):
        Dashboard.__init__(self, orientation)


class DashboardEast(Dashboard):

    """
        Dashboard sub-class dor eastward orientation.
    """

    def __init__(self, orientation):
        Dashboard.__init__(self, orientation)
