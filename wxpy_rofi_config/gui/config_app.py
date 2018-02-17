# pylint: disable=W,C,R

# pylint: disable=no-name-in-module
from wx import (
    App
)
# pylint: enable=no-name-in-module

# from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(App):

    def OnInit(self):
        frame = ConfigFrame()
        frame.Show()
        return True


def cli():
    if '__main__' == __name__:
        app = ConfigApp(False)
        app.MainLoop()

cli()
