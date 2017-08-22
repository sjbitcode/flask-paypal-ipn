import requests
from flask import current_app, render_template
# from sqlalchemy import exc

# from app import app, db
# from .models import IPN
from . import email_texts
from . import settings


def format_price(amount, currency=u'$'):
    return u'{0}{1:.2f}'.format(currency, amount)


def check_email_api_response(email_type, **email_kwargs):
    try:
        status, text = email_api(**email_kwargs)
        if status != 200:
            current_app.logger.debug(
                'Unsuccessful {} email transaction. status {}, text {}'
                .format(email_type, status, text)
            )
        elif status == 200:
            current_app.logger.info(
                'Successful {} email transaction. status {}, text{}'
                .format(email_type, status, text)
            )
    except Exception as e:
        current_app.logger.error('Error sending {} email: {}'.format(email_type, e))


def send_warning_email(warning_email_text, category=None):
    if category == 'validate_receiver':
        body_text = email_texts.validate_receiver + warning_email_text

    elif category == 'duplicate_transaction':
        body_text = email_texts.duplicate_transaction + warning_email_text

    elif category == 'duplicate_completed_transaction':
        body_text = email_texts.duplicate_completed_transaction + warning_email_text

    elif category == 'completed_different_transaction':
        body_text = email_texts.completed_different_transaction + warning_email_text

    email_kwargs = {
        'from_name': settings.SENDER_NAME,
        'from_email': settings.SENDER_EMAIL,
        'to_email': settings.INFO_EMAIL,
        'subject': 'Suspicious Payment',
        'body_html': None,
        'body_text': body_text
    }

    check_email_api_response('Warning', **email_kwargs)


def send_thank_you_email(**kwargs):
    '''
    Prepares the thank you email with
    following parameters:
        (donor) first_name,
        amount,
        (donor) email
    '''
    first_name = kwargs.get('first_name')
    amount = format_price(float(kwargs.get('amount')))
    email = 'sjbitcode@gmail.com' or kwargs.get('email')
    signup_form_link = kwargs.get('signup_form_link') or settings.MAILCHIMP_SIGNUP_FORM_LINK

    body_text = email_texts.thank_you_email_text.format(
        first_name,
        amount,
        signup_form_link
    )

    body_html = render_template(
        'donation.html',
        first_name=first_name,
        amount=amount,
        signup_form_link=signup_form_link
    )

    email_kwargs = {
        'from_name': settings.SENDER_NAME,
        'from_email': settings.SENDER_EMAIL,
        'to_email': email,
        'subject': 'Thank You for your Donation!',
        'body_html': body_html,
        'body_text': body_text
    }

    check_email_api_response('Thank You', **email_kwargs)


def email_api(**kwargs):
    '''
    Sends email through Mailgun api using
    mailgun url and mailgun api key and parameters.
    '''
    from_name = kwargs.get('from_name')
    from_email = kwargs.get('from_email')
    to_email = kwargs.get('to_email')
    subject = kwargs.get('subject')
    body_html = kwargs.get('body_html')
    body_text = kwargs.get('body_text')

    mailgun_url = '{0}/messages'.format(settings.MAILGUN_URL)
    mailgun_api_key = settings.MAILGUN_API_KEY

    request = requests.post(
        mailgun_url,
        auth=('api', mailgun_api_key),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'from': '{0} <{1}>'.format(from_name, from_email),
            'to': to_email,
            'subject': subject,
            'text': body_text,
            'html': body_html
        }
    )

    return (request.status_code, request.text)


# def validate_amounts(payment_gross, option_selection1, warning_email_text):
#     payment_gross = float(payment_gross)
#     payment_values = str(['${0:.2f}'.format(x) for x in settings.PAYMENT_OPTIONS])
#
#     # If payment is not 'Other' and amount paid is not a donation amount listed
#     if (option_selection1 != 'Other') and (payment_gross not in settings.PAYMENT_OPTIONS):
#         # amount paid is not equal to amount supposed to pay
#         ipn_log(
#             'Suspicious Payment - Someone paid ${0:.2f} instead of {1}.'
#             .format(
#                 payment_gross,
#                 payment_values
#             )
#         )
#
#         validate_amounts_text = email_texts.validate_amount.format(payment_values)
#         body_text = validate_amounts_text + warning_email_text
#
#         email_kwargs = {
#             'from_name': settings.SENDER_NAME,
#             'from_email': settings.SENDER_EMAIL,
#             'to_email': settings.INFO_EMAIL,
#             'subject': 'Suspicious Payment',
#             'body_html': None,
#             'body_text': body_text
#         }
#
#         check_email_api_response('Amount Validation', **email_kwargs)
#
#         return False
#     else:
#         return True
