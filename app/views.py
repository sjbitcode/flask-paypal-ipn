import requests

from flask import (
    Blueprint, current_app,
    request, render_template,
    url_for, redirect
)
from sqlalchemy import exc
from werkzeug.datastructures import ImmutableOrderedMultiDict

from .database import db
from . import settings, email_texts
from .forms import EmailForm
from .models import IPN
from .utils import (
    send_thank_you_email, send_warning_email
)


main = Blueprint(name='main', import_name=__name__)


def write_ipn(request_dict, instance=None, instance_query=None):
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
            print('Created new IPN entry!!!!!!!!!!!')
            current_app.logger.info('Created new IPN entry')
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
            print('Updated IPN entry!!!!!!!!!!!')
            return
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            raise

    # with current_app.app_context():
    #     if not instance:
    #         try:
    #             instance = IPN(**kwargs)
    #             db.session.add(instance)
    #             db.session.commit()
    #             print('Created new IPN entry!!!!!!!!!!!')
    #             current_app.logger.info('Created new IPN entry')
    #             return
    #         except exc.IntegrityError as e:
    #             db.session.rollback()
    #             current_app.logger.error(e)
    #             print(e)
    #             raise
    #     else:
    #         # don't overwrite the primary key
    #         kwargs.pop('txn_id')
    #         try:
    #             instance_query.update(kwargs)
    #             db.session.commit()
    #             current_app.logger.info('Updated IPN entry.')
    #             print('Updated IPN entry!!!!!!!!!!!')
    #             return
    #         except Exception as e:
    #             current_app.logger.error(e)
    #             print(e)
    #             raise


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/email-template', methods=['GET'])
def donation_display_template():
    return render_template('donation_display_template.html')


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
                'signup_form_link': form.data.get('signup_form_link') or 'http://eepurl.com/cZBoOX'
            })

            return redirect(url_for('main.success'))

    return render_template('send_email.html', form=form)


@main.route('/ipn', methods=['POST'])
def ipn():
    arg = ''

    # Setting storage class to ordered dict.
    request.parameter_storage_class = ImmutableOrderedMultiDict

    # Create arg list.
    values = request.form
    for x, y in values.items():
        arg += "&{x}={y}".format(x=x, y=y)

    # Create validate url and send back to Paypal.
    validate_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate{arg}' \
        .format(arg=arg)
    r = requests.get(validate_url)

    print(r.content)
    print(r.text)

    if r.text == 'VERIFIED':

        print("PayPal transaction was verified successfully.")
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
                                mc_currency, mc_gross
                            )

        # Verify that we are the intended recipient.
        if (receiver_email == settings.PAYPAL_RECEIVER_EMAIL):
            # print('ITS FOR US!!!!!')

            query = IPN.query.filter_by(txn_id=txn_id)
            ipn_obj = query.first()
            new_status = payment_status
            # print('IPN_OBJ IS ', ipn_obj)

            # If ipn entry saved in database
            if ipn_obj:
                past_status = ipn_obj.payment_status

                # If existing ipn status not Completed
                if past_status != 'Completed':

                    # ... and new status is different
                    if new_status != past_status:
                        # print('UPDATING AN EXISTING IPN')
                        # update ipn entry
                        write_ipn(
                            request.form, instance=ipn_obj,
                            instance_query=query
                        )

                        # If status was updated to Completed
                        if new_status == 'Completed':
                            # print('UPDATING TO COMPLETED STATUS')

                            # Send thank you email
                            current_app.logger.info('Sending email...')
                            send_thank_you_email(
                                **{
                                    'first_name': first_name,
                                    'email': payer_email,
                                    'amount': payment_gross or mc_gross
                                })

                    else:
                        # and new status is same but not Complete, warning!
                        current_app.logger.warning('Received ipn with duplicate txn_id and status')
                        print('DUPLICATE TXN_ID RECEIVED')
                        # current_app.logger.info('Sending warning email...')
                        send_warning_email(
                            warning_email_text,
                            category='duplicate_transaction'
                        )
                else:
                    # If existing ipn status is Completed

                    # ... and new status is also Completed.
                    if new_status == 'Completed':
                        current_app.logger.warning('Received duplicated complete ipn.')
                        print('OLD AND COMPLETED IPN ENTRY')
                        # ipn_log('Sending warning email')
                        send_warning_email(
                            warning_email_text,
                            category='duplicate_completed_transaction'
                        )

                    # ... and new status is not Completed, but different.
                    else:
                        current_app.logger.warning('Received ipn for completed ipn entry.')
                        print('ALREADY COMPLETED IPN ENTRY')
                        # ipn_log('Sending warning email')
                        send_warning_email(
                            warning_email_text,
                            category='completed_different_transaction'
                        )
            else:
                # Create entry in database.
                print('CREATING NEW IPN ENTRY')
                current_app.logger.info('Creating new ipn entry.')
                write_ipn(request.form)

                # If new status complete, send email.
                if new_status == 'Completed':
                    send_thank_you_email(
                        **{
                            'first_name': first_name,
                            'email': payer_email,
                            'amount': payment_gross or mc_gross
                        }
                    )
        else:
            # Another merchant accidentally or intentionally used our IPN url.
            print('Other merchant used IPN url!')
            # SEND WARNING EMAIL
            current_app.logger.warning('Other merchant used IPN url!')
            # ipn_log('Sending warning email...')
            send_warning_email(warning_email_text, category='validate_receiver')
    else:
        print('Paypal IPN string {arg} did not validate'.format(arg=arg))

        # Create success log entry.
        data = 'FAILURE\n'+str(values)+'\n'
        current_app.logger.error(data)

    return r.text
