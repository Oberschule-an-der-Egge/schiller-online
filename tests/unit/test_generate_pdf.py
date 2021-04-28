from contextlib import contextmanager

import pytest

from src.main import create_app
from src.services import generate_pdf


@pytest.mark.skip(reason='prevented write-to-disk in conftest')
def test_create_pdf(client, monkeypatch):
    rv = client.get('/')
    monkeypatch.setattr(generate_pdf, 'create_html', lambda x: None)
    monkeypatch.setattr(generate_pdf, 'convert_to_pdf', lambda x, y: None)
    filename = 'file.xyz'
    rv = generate_pdf.create_pdf(filename)
    assert 'output/file.xyz' in rv
