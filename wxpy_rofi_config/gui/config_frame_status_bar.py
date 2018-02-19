# coding=utf8

"""This file provides ConfigFrameStatusBar"""

# pylint: disable=too-many-ancestors

from wx import (
    StatusBar,
)
from wx.lib.pubsub import pub


class ConfigFrameStatusBar(StatusBar):
    """ConfigFrameStatusBar collects status bar construction and actions"""

    def __init__(self):
        StatusBar.__init__(self)
        pub.subscribe(self.update, 'status_update')
        pub.subscribe(self.clear, 'status_clear')

    def update(self, status):
        """Updates the status bar text"""
        self.SetStatusText(status, 0)

    def clear(self):
        """Clears the status text"""
        self.SetStatusText('', 0)
