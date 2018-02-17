# coding=utf8

"""This file provides the ConfigApp class and cli access"""

from wx import (
    App
)

from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(App):
    """ConfigApp provides the main GUI"""

    def __init__(self):
        App.__init__(self)
        frame = ConfigFrame()
        frame.Show()


def cli():
    """Checks if the module has been loaded via the CLI"""
    if '__main__' == __name__:
        app = ConfigApp()
        app.MainLoop()

cli()
