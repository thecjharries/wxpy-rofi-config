# pylint: disable=missing-docstring

from __future__ import print_function

from mock import MagicMock, patch


def test_on_init():
    from wxpy_rofi_config import config_app  # pylint: disable=no-name-in-module
    with patch('wxpy_rofi_config.gui.config_app.App', MagicMock()):
        with patch('wxpy_rofi_config.gui.config_app.ConfigFrame') as mock_frame:
            config_app.ConfigApp()
            mock_frame.assert_called_once_with()


def test_cli():
    from wxpy_rofi_config import config_app  # pylint: disable=no-name-in-module
    with patch.object(config_app, "ConfigApp", return_value=MagicMock()) as mock_app:
        with patch.object(config_app, "__name__", "__main__"):
            config_app.cli()
            mock_app.assert_called_once_with()
