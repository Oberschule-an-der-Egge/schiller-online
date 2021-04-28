# App Variables
from pathlib import Path

VERSION = '1.0'
JAHRGANG = 20

# Debug Output in Flask
DEBUG = True

# Secret Key Example
SECRET_KEY = 'ThisKeyisNotSecretAtAll'

# Production Config
URL_UPLAN = None
ROOT_PATH = Path(__file__).parent.parent.parent
OUTPUT_PATH = ROOT_PATH.joinpath('output')
LOG_FILE = 'user.log'

# Redis
REDIS_SOCKET = None
REDIS_PASS = None

# Mailing
MAIL_SENDER = None
MAIL_RECIPIENT = None
MAIL_SERVER = None
MAIL_PORT = None
MAIL_LOGIN = None
MAIL_PASSWORD = None
