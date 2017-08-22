from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Email, Optional, URL, Regexp


class EmailForm(FlaskForm):
    first_name = StringField(
        'Donor first name',
        validators=[
            InputRequired(message='The donor first name is required.'),
            Regexp('^[a-zA-Z]+$', message="First name must contain only letters")
        ])

    email = StringField(
        'Donor email address',
        validators=[
            InputRequired(message='The donor email address is required.'),
            Email()
        ])

    amount = DecimalField(
        'Donation amount',
        places=2,
        validators=[
            InputRequired(message='The donation amount is required.')
        ])

    signup_form_link = StringField(
        'MailChimp Signup Link (optional)',
        validators=[
            Optional(), URL()
        ])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        try:
            print(self.amount.data)
            float(self.amount.data)
        except ValueError:
            self.amount.errors.append(
                'Amount must be valid decimal number.'
            )
        if 0 >= float(self.amount.data):
            self.amount.errors.append(
                'Amount must be nonzero positive decimal number.'
            )
            return False
        return True
