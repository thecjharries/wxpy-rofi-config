# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from mock import MagicMock, patch


def test_cli():
    from wxpy_rofi_config import launcher  # pylint: disable=no-name-in-module
    with patch.object(launcher, "ConfigApp", return_value=MagicMock()) as mock_app:
        with patch.object(launcher, "__name__", "__main__"):
            launcher.main()
            mock_app.assert_called_once_with()
