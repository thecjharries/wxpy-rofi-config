# coding=utf8

"""This file provides ConfigFrameStatusBar"""

# pylint: disable=too-many-ancestors

from wx import (
    StatusBar,
)
from wx.lib.pubsub.pub import subscribe


class ConfigFrameStatusBar(StatusBar):
    """ConfigFrameStatusBar collects status bar construction and actions"""

    def __init__(self, parent):
        StatusBar.__init__(self, parent)
        subscribe(self.update, 'status_update')
        subscribe(self.clear, 'status_clear')

    def update(self, data):
        """Updates the status bar text"""
        self.SetStatusText(data, 0)

    def clear(self):
        """Clears the status text"""
        self.SetStatusText('', 0)
