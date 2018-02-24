# coding=utf8

"""This file provides ModiLauncher"""

from subprocess import call

from wx import (
    ID_OK,
    SingleChoiceDialog
)


class ModiLauncher(object):
    """ModiLauncher provides a simple listbox that can launch a modi"""

    DEFAULT_PROMPT = 'Select a modi'

    def __init__(self, available_modi, prompt=None):
        self.modi = available_modi
        if prompt is None:
            self.prompt = self.DEFAULT_PROMPT
        else:
            self.prompt = prompt
        self.select_and_launch()

    def select_modi(self):
        """Creates a dialog to select an available modi"""
        with SingleChoiceDialog(None, self.prompt, 'modi', self.modi) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetStringSelection()
        return None

    def select_and_launch(self):
        """Prompts the user to pick a modi to run"""
        desired_modi = self.select_modi()
        if desired_modi:
            self.launch_modi(desired_modi)

    @staticmethod
    def launch_modi(modi_to_launch):
        """Launches the provided modi"""
        call(['rofi', '-show', modi_to_launch])
