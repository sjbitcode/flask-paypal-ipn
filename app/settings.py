import os


def get_env(key, default=None):
    return os.environ.get(key, default)


HOST = get_env('HOST')
PORT = int(get_env('PORT', ''))
DEBUG = get_env('DEBUG', False) in ['True', 'true']

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False

PAYPAL_URL = get_env('PAYPAL_URL')
PAYPAL_SANDBOX_URL = get_env('PAYPAL_SANDBOX_URL')
PAYPAL_RECEIVER_EMAIL = get_env('PAYPAL_RECEIVER_EMAIL')

# Mailgun Credentials
MAILGUN_API_KEY = get_env('MAILGUN_API_KEY')
MAILGUN_URL = get_env('MAILGUN_URL')
MAILGUN_SANDBOX_URL = get_env('MAILGUN_SANDBOX_URL')
MAILGUN_SANDBOX_AUTHORIZED_RECIPIENT = get_env(
    'MAILGUN_SANDBOX_AUTHORIZED_RECIPIENT')

SECRET_KEY = get_env('SECRET_KEY')
WTF_CSRF_ENABLED = True

SENDER_EMAIL = get_env('SENDER_EMAIL')
SENDER_NAME = get_env('SENDER_NAME')
INFO_EMAIL = get_env('INFO_EMAIL')

PAYMENT_OPTIONS = [float(x) for x in get_env('PAYMENT_OPTIONS').split(',')]

MAILCHIMP_SIGNUP_FORM_LINK = get_env('MAILCHIMP_SIGNUP_FORM_LINK')
