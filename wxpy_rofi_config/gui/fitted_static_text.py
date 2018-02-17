# coding=utf8

"""This file provides the FittedStaticText class"""

from wx import (
    BORDER_NONE,
    Control,
    ID_ANY,
    StaticText,
)


class FittedStaticText(Control):
    """
    FittedStaticText is an attempt to get StaticTexts to resize with the rest
    of the application
    """

    def __init__(self, parent, label="", name="fitted_static_text"):
        Control.__init__(
            self,
            parent=parent,
            id=ID_ANY,
            name=name,
            style=BORDER_NONE
        )
        self.text = StaticText(self, -1, label)
        self.set_label(label)

    def set_label(self, label):
        """Updates the label"""
        self.label = label
        self.fit_label()

    def resize(self):
        """Resizes the element"""
        self.fit_label()
        self.text.SetSize(self.GetSize())
        self.fit_label()

    def fit_label(self):
        """Fits the element's size"""
        self.text.Freeze()
        self.text.SetLabel(self.label)
        self.text.Wrap(self.GetSize().width)
        self.text.Thaw()
