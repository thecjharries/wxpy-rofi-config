# pylint: disable=W,C,R

# pylint: disable=no-name-in-module
from wx import (
    BORDER_NONE,
    Control,
    ID_ANY,
    StaticText,
)
# pylint: enable=no-name-in-module


class FittedStaticText(Control):

    def __init__(self, parent, label="", name="fitted_static_text"):
        Control.__init__(
            self,
            parent=parent,
            id=ID_ANY,
            name=name,
            style=BORDER_NONE
        )
        self.text = StaticText(self, -1, label)
        self.SetLabel(label)

    def SetLabel(self, label):
        self.label = label
        self.fit()

    def resize(self):
        self.fit()
        self.text.SetSize(self.GetSize())
        self.fit()

    def fit(self):
        self.text.Freeze()
        self.text.SetLabel(self.Label)
        self.text.Wrap(self.GetSize().width)
        self.text.Thaw()
