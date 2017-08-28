import requests
from flask import (
    Blueprint, current_app,
    request, render_template,
    url_for, redirect)
from werkzeug.datastructures import ImmutableOrderedMultiDict

from . import settings, email_texts
from .forms import EmailForm
from .models import IPN
from .utils import (
    send_thank_you_email,
    send_warning_email,
    write_ipn)


main = Blueprint(name='main', import_name=__name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/email-template', methods=['GET'])
def donation_display_template():
    return render_template('donation_display_template.html',
        signup_form_link=settings.MAILCHIMP_SIGNUP_FORM_LINK)


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@main.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


@main.route('/email', methods=['GET', 'POST'])
def manual_send_email():
    form = EmailForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():

            send_thank_you_email(**{
                'first_name': form.data.get('first_name'),
                'email': form.data.get('email'),
                'amount': form.data.get('amount'),
                'signup_form_link': form.data.get('signup_form_link')})

            return redirect(url_for('main.success'))

    return render_template('send_email.html',
        form=form,
        signup_form_link=settings.MAILCHIMP_SIGNUP_FORM_LINK,
        sender_email=settings.SENDER_EMAIL)


@main.route('/ipn', methods=['POST'])
def ipn():
    '''
    Process incoming Paypal IPN.
    If IPN is verified, perform several checks
    before updating database and sending emails.

    Conditions:
    1 - An existing IPN's status changes to Completed
        --> send thank-you email.

    2 - A new IPN has same transaction id and status
        as an existing, incomplete IPN
        --> send warning email.

    3 - A new IPN has same transaction id and status
        as an existing, completed IPN
        --> send warning email.

    4 - A new IPN has same transaction id and different
        status of an existing, completed IPN
        --> send warning email.

    5 - A new IPN entry is created whose status is Completed
        --> send thank-you email.

    6 - A new IPN has a different receiver email than what
        is registered on our Paypal account
        --> send warning email.
    '''

    # Verify Paypal IPN
    arg = ''
    request.parameter_storage_class = ImmutableOrderedMultiDict
    values = request.form

    for x, y in values.items():
        arg += "&{x}={y}".format(x=x, y=y)

    validate_url = '{url}?cmd=_notify-validate{arg}'.format(
        url=settings.PAYPAL_URL, arg=arg)

    r = requests.get(validate_url)

    if r.text == 'VERIFIED':

        current_app.logger.info(
            'Paypal transaction was verified successfully.')

        print(request.form)

        # Collect useful info for the following.
        txn_id = request.form.get('txn_id', None)
        receiver_email = request.form.get('receiver_email', None)
        payer_email = request.form.get('payer_email', None)
        first_name = request.form.get('first_name', None)
        last_name = request.form.get('last_name', None)
        payment_status = request.form.get('payment_status', None)
        payment_date = request.form.get('payment_date', None)
        item_name = request.form.get('item_name', None)
        item_number = request.form.get('item_number', None)
        option_selection1 = request.form.get('option_selection1', None)
        payment_gross = request.form.get('payment_gross', None)
        mc_currency = request.form.get('mc_currency', None)
        mc_gross = request.form.get('mc_gross', None)

        # Construct some details in case we have to send a warning email.
        warning_email_text = email_texts.ipn_info_warning_email.format(
                                txn_id, receiver_email, payer_email,
                                first_name, last_name, payment_status,
                                payment_date, item_name, item_number,
                                option_selection1, payment_gross,
                                mc_currency, mc_gross)

        # Verify that we are the intended recipient.
        if (receiver_email == settings.PAYPAL_RECEIVER_EMAIL):
            query = IPN.query.filter_by(txn_id=txn_id)
            ipn_obj = query.first()
            new_status = payment_status

            if ipn_obj:
                past_status = ipn_obj.payment_status

                if past_status != 'Completed':

                    # New status is different
                    if new_status != past_status:

                        # update IPN entry
                        current_app.logger.info('Updating IPN entry.')
                        write_ipn(
                            request.form, instance=ipn_obj,
                            instance_query=query)

                        # New status updated to Complete (condition 1)
                        if new_status == 'Completed':
                            current_app.logger.info('Sending thank you email.')
                            send_thank_you_email(**{
                                    'first_name': first_name,
                                    'email': payer_email,
                                    'amount': payment_gross or mc_gross})

                    else:

                        # New status same as past, not Complete (condition 2)
                        current_app.logger.warning(
                            'Received duplicate incomplete IPN.')
                        send_warning_email(
                            warning_email_text,
                            category='duplicate_transaction')
                else:

                    # If existing ipn status is Completed (condition 3)
                    if new_status == 'Completed':
                        current_app.logger.warning(
                            'Received duplicated complete IPN.')
                        send_warning_email(
                            warning_email_text,
                            category='duplicate_completed_transaction')

                    else:

                        # New status not Completed (condition 4)
                        current_app.logger.warning(
                            'Received IPN for already completed IPN entry.')
                        send_warning_email(
                            warning_email_text,
                            category='completed_different_transaction')
            else:

                # Create entry in database.
                current_app.logger.info('Creating new IPN entry.')
                write_ipn(request.form)

                # If new status complete (condition 5)
                if new_status == 'Completed':
                    current_app.logger.info('Sending thank you email.')
                    send_thank_you_email(**{
                            'first_name': first_name,
                            'email': payer_email,
                            'amount': payment_gross or mc_gross})
        else:

            # Our IPN url was accidentally or intentionally used (condition 6)
            current_app.logger.warning('Receiver email incorrect.')
            send_warning_email(
                warning_email_text,
                category='validate_receiver')
    else:
        print('Paypal IPN string {arg} did not validate'.format(arg=arg))

        # Create success log entry.
        data = 'Paypal IPN string {arg} did not validate\n'.format(arg=arg)
        data += 'FAILURE\n'+str(values)+'\n'
        current_app.logger.error(data)

    return r.text
