from unittest.mock import mock_open, patch

import pytest

from src.main import create_app
from src.services import logging


@pytest.mark.skip(reason='how to mock session["token"]')
def test_log_user_session():
    app = create_app()
    open_mock = mock_open()
    with patch("logging.open", open_mock, create=True):
        with app.app_context():
            logging.log_user_session()

    open_mock.assert_called_with('user.log', 'a+')
    open_mock.return_value.write.assert_called_with('')
