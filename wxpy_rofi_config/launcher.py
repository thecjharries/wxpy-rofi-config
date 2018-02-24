# coding=utf8
# pylint: disable=W,C,R
# pylint: disable=no-member

from wxpy_rofi_config.gui import ConfigApp


def main():
    if '__main__' == __name__:
        app = ConfigApp()
        app.MainLoop()

main()
