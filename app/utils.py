import requests
from flask import current_app, render_template
from sqlalchemy import exc

from .database import db
from .models import IPN
from . import email_texts
from . import settings


def format_price(amount, currency=u'$'):
    return u'{0}{1:.2f}'.format(currency, amount)


def write_ipn(request_dict, instance=None, instance_query=None):
    '''
    Create or update IPN entry.
    '''

    kwargs = {}

    kwargs['txn_id'] = request_dict.get('txn_id')
    kwargs['receiver_email'] = request_dict.get('receiver_email', None)
    kwargs['payer_email'] = request_dict.get('payer_email', None)
    kwargs['first_name'] = request_dict.get('first_name', None)
    kwargs['last_name'] = request_dict.get('last_name', None)
    kwargs['payment_status'] = request_dict.get('payment_status', None)
    kwargs['payment_date'] = request_dict.get('payment_date', None)
    kwargs['item_name'] = request_dict.get('item_name', None)
    kwargs['item_number'] = request_dict.get('item_number', None)
    kwargs['option_selection1'] = request_dict.get('option_selection1', None)
    kwargs['payment_gross'] = float(request_dict.get('payment_gross', 0))
    kwargs['payment_fee'] = float(request_dict.get('payment_fee', 0))
    kwargs['mc_gross'] = float(request_dict.get('mc_gross', 0))
    kwargs['mc_fee'] = float(request_dict.get('mc_fee', 0))
    kwargs['mc_currency'] = request_dict.get('mc_currency', None)
    kwargs['memo'] = request_dict.get('memo', None)

    if not instance:
        try:
            instance = IPN(**kwargs)
            db.session.add(instance)
            db.session.commit()
            current_app.logger.info('Created IPN entry.')
            return
        except exc.IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(e)
            print(e)
            raise
    else:
        # don't overwrite the primary key
        kwargs.pop('txn_id')
        try:
            instance_query.update(kwargs)
            db.session.commit()
            current_app.logger.info('Updated IPN entry.')
            return
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            raise


def send_email_api(email_type, **email_kwargs):
    '''
    Takes an email_type(string), and email_kwargs(dict).

    Calls the email_api function with email_kwargs and logs
    status of email sending.
    '''

    email_log_line = '{from_email} -> {to_email}'.format(**email_kwargs)

    try:
        status, text = email_api(**email_kwargs)
        if status != 200:
            current_app.logger.debug(
                'Unsuccessful {} email transaction: {} \nstatus {}, text {}'
                .format(email_type, email_log_line, status, text))

        elif status == 200:
            current_app.logger.info(
                'Successful {} email transaction: {} \nstatus {}, text {}'
                .format(email_type, email_log_line, status, text))

    except Exception as e:
        current_app.logger.error(
            'Error sending {} email: {} \nerror {}'.format(
                email_type, email_log_line, e))


def send_warning_email(warning_email_text, category=None):
    '''
    Sends warning emails based on warning type.
    All warning emails include IPN payment details.

    The rest of the values for the warning email
    are taken from settings.

    Constructs dict specified in email_api function.
    '''

    # Render appropriate text email body.
    if category == 'validate_receiver':
        body_text = email_texts.validate_receiver + warning_email_text

    elif category == 'duplicate_transaction':
        body_text = email_texts.duplicate_transaction + warning_email_text

    elif category == 'duplicate_completed_transaction':
        body_text = (
            email_texts.duplicate_completed_transaction +
            warning_email_text)

    elif category == 'completed_different_transaction':
        body_text = (
            email_texts.completed_different_transaction +
            warning_email_text)

    # Construct email_api dict.
    email_kwargs = {
        'from_name': settings.WARNING_SENDER_NAME,
        'from_email': settings.WARNING_SENDER_EMAIL,
        'to_email': settings.WARNING_RECEIVER_EMAIL,
        'subject': settings.WARNING_SUBJECT_LINE,
        'body_html': None,
        'body_text': body_text}

    send_email_api('Warning', **email_kwargs)


def send_thank_you_email(**kwargs):
    '''
    Sends thank you email
    based on donor first name, amount donated,
    donor email, optional signup form link.

    The rest of the values for the thank you email
    are taken from settings. Email template is rendered
    using 'donation.html' template.

    Constructs dict specified in email_api function.
    '''

    first_name = kwargs.get('first_name')
    amount = format_price(float(kwargs.get('amount')))
    email = kwargs.get('email')

    signup_form_link = (
        kwargs.get('signup_form_link') or
        settings.MAILCHIMP_SIGNUP_FORM_LINK)

    # Render text and html email body.
    body_text = email_texts.thank_you_email_text.format(
        first_name,
        amount,
        signup_form_link)

    body_html = render_template(
        'donation.html',
        first_name=first_name,
        amount=amount,
        signup_form_link=signup_form_link)

    # Construct email_api dict.
    email_kwargs = {
        'from_name': settings.SENDER_NAME,
        'from_email': settings.SENDER_EMAIL,
        'to_email': email,
        'subject': settings.SUBJECT_LINE,
        'body_html': body_html,
        'body_text': body_text}

    send_email_api('Thank You', **email_kwargs)


def email_api(**kwargs):
    '''
    Sends email through Mailgun api using
    mailgun url and mailgun api key and parameters.

    Accepts a dict with the following keys:
    {
        from_name,
        from_email,
        to_email,
        subject,
        body_html,
        body_text
    }
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
            'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'from': '{0} <{1}>'.format(from_name, from_email),
            'to': to_email,
            'subject': subject,
            'text': body_text,
            'html': body_html}
    )

    return (request.status_code, request.text)
