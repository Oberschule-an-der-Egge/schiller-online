import fakeredis
import pytest
import xlsxwriter

from src.main import create_app
from src.services import cache, logging, generate_excel, generate_pdf


class FakeRedisConnection:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print('called')
            cls.instance = fakeredis.FakeStrictRedis(decode_responses=True)
        return cls.instance


@pytest.fixture
def client(monkeypatch):

    monkeypatch.setattr(cache, 'RedisConnection', FakeRedisConnection)

    # Don't write files to disk
    monkeypatch.setattr(logging, 'log_user_session', lambda: 'no-log')
    monkeypatch.setattr(generate_pdf, 'save_html', lambda _: 'no-html')
    monkeypatch.setattr(generate_pdf, 'convert_to_pdf', lambda x, y: 'no-pdf')
    monkeypatch.setattr(generate_excel, 'get_workbook', lambda path: xlsxwriter.Workbook(path, {'in_memory': True}))
    monkeypatch.setattr(xlsxwriter.Workbook, 'close', lambda _: 'no-xlsx')

    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # db here
            pass
        yield client
