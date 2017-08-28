import os


def get_env(key, default=None):
    return os.environ.get(key, default)


HOST = get_env('HOST')
PORT = int(get_env('PORT', ''))
DEBUG = get_env('DEBUG', False) in ['True', 'true']
SECRET_KEY = get_env('SECRET_KEY')
WTF_CSRF_ENABLED = True

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False

PAYPAL_RECEIVER_EMAIL = get_env('PAYPAL_RECEIVER_EMAIL')
PAYPAL_URL = get_env('PAYPAL_URL')

MAILGUN_API_KEY = get_env('MAILGUN_API_KEY')
MAILGUN_URL = get_env('MAILGUN_URL')
MAILGUN_SANDBOX_AUTHORIZED_RECIPIENT = get_env(
    'MAILGUN_SANDBOX_AUTHORIZED_RECIPIENT')

SENDER_EMAIL = get_env('SENDER_EMAIL')
SENDER_NAME = get_env('SENDER_NAME')
SUBJECT_LINE = get_env('SUBJECT_LINE')

WARNING_SENDER_EMAIL = get_env('WARNING_SENDER_EMAIL')
WARNING_SENDER_NAME = get_env('WARNING_SENDER_NAME')
WARNING_RECEIVER_EMAIL = get_env('WARNING_RECEIVER_EMAIL')
WARNING_SUBJECT_LINE = get_env('WARNING_SUBJECT_LINE')

MAILCHIMP_SIGNUP_FORM_LINK = get_env('MAILCHIMP_SIGNUP_FORM_LINK')
