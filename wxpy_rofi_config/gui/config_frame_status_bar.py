# coding=utf8

"""This file provides ConfigFrameStatusBar"""

# pylint: disable=too-many-ancestors

from wx import (
    StatusBar,
)
from pydispatch.dispatcher import Any, connect


class ConfigFrameStatusBar(StatusBar):
    """ConfigFrameStatusBar collects status bar construction and actions"""

    def __init__(self, parent):
        StatusBar.__init__(self, parent)
        connect(self.update, signal='status_update', sender=Any)
        connect(self.clear, signal='status_clear', sender=Any)

    def update(self, data):
        """Updates the status bar text"""
        self.SetStatusText(data, 0)

    def clear(self):
        """Clears the status text"""
        self.SetStatusText('', 0)
