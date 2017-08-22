import os


def get_env(key, default=None):
    return os.environ.get(key, default)


HOST = get_env('HOST')
PORT = int(get_env('PORT', ''))
DEBUG = get_env('DEBUG', False) in ['True', 'true']

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

# MySQL Credentials.
MYSQL_USERNAME = get_env('MYSQL_USERNAME')
MYSQL_PASSWORD = get_env('MYSQL_PASSWORD')
MYSQL_HOST = get_env('MYSQL_HOST')
MYSQL_DATABASE = get_env('MYSQL_DATABASE')

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
                            MYSQL_USERNAME,
                            MYSQL_PASSWORD,
                            MYSQL_HOST,
                            MYSQL_DATABASE
                          )
SQLALCHEMY_TRACK_MODIFICATIONS = False

PAYPAL_RECEIVER_EMAIL = get_env('PAYPAL_RECEIVER_EMAIL')

# Mailgun Credentials
MAILGUN_API_KEY = get_env('MAILGUN_API_KEY')
MAILGUN_URL = get_env('MAILGUN_URL')
MAILGUN_SANDBOX_URL = get_env('MAILGUN_SANDBOX_URL')

SECRET_KEY = get_env('SECRET_KEY')
WTF_CSRF_ENABLED = True

SENDER_EMAIL = get_env('SENDER_EMAIL')
SENDER_NAME = get_env('SENDER_NAME')
INFO_EMAIL = get_env('INFO_EMAIL')

PAYMENT_OPTIONS = [float(x) for x in get_env('PAYMENT_OPTIONS').split(',')]

MAILCHIMP_SIGNUP_FORM_LINK = get_env('MAILCHIMP_SIGNUP_FORM_LINK')
