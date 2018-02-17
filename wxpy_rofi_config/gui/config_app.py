"""This file provides the ConfigApp class and cli access"""


from wx import (
    App
)


# from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(App):
    """ConfigApp provides the main GUI"""

    def OnInit(self):  # pylint:disable=invalid-name
        """Initializes the GUI"""
        frame = ConfigFrame()
        frame.Show()
        return True


def cli():
    """Checks if the module has been loaded via the CLI"""
    if '__main__' == __name__:
        app = ConfigApp(False)
        app.MainLoop()

cli()
