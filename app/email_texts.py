
# text body for thank you email.
thank_you_email_text = (
    'Dear {0},\n\n'
    'Thank you for making a donation to Cook Play Live Inc. '
    'Your gift of {1} will have a profound impact in our mission to '
    'promote healthier eating and cooking habits and support our work in '
    'New York City out-of-school-time children and youth programs.\n\n'
    'Now you might be able to double or even triple the impact of '
    'your gift through your employer’s matching gift program! '
    'Many companies match their employees’ charitable giving to '
    'Cook Play Live, meaning that your gift can do even more to '
    'help us foster healthy eating behavior.\n\n\n'
    'Warm Regards,\n\n'
    'Fen Yee Teh\n'
    'Founding Director\n'
    'Cook Play Live Inc.'
    '\n\n\n\n'
    'Our mailing address is:\n'
    '104 West 70th Street Suite 11C\n'
    'New York NY 10023'
    '\n\n'
    'Subscribe to our Newsletter!\n'
    '{2}'

)

# text body for warning validate receiver email.
validate_receiver = (
    'This is a message to inform you that a recent Paypal '
    'transaction was made and the receiver_email is not an '
    'email address registered in your Paypal account.\n\n'
    'This could mean that the payment is being sent to a '
    'fraudster\'s account instead of yours '
    'or that a merchant has accidentally or intentionally '
    'used your Paypal IPN url.'
    '\n\n'
    'The automatic thank you email was not sent because '
    'of this suspicious activity.'
    '\n\n'
    'If this email was sent in error, you can still send '
    'the thank you email by using this link.'
)

# text body for warning duplicate noncomplete transaction email.
duplicate_transaction = (
    'This is a message to inform you that a recent Paypal '
    'transaction was made and the transaction id and status '
    'of the payment is a duplicate of one that has already '
    'been made.\n\n'
    'This could mean that a fraudster has reused an old transaction\'s '
    'id and payment status (check payment status).'
    '\n\n'
    'The automatic thank you email was not sent because '
    'of this suspicious activity.'
    '\n\n'
    'If this email was sent in error, you can still send '
    'the thank you email by using this link.'
)

# text body for warning duplicate completed transaction email.
duplicate_completed_transaction = (
    'This is a message to inform you that a recent Paypal '
    'transaction was made and the transaction id and completed status '
    'of the payment is a duplicate of an existing completed transaction.'
    '\n\n'
    'This could mean that a fraudster has reused an old, '
    'completed transaction '
    '(check payment status).'
    '\n\n'
    'The automatic thank you email was not sent because '
    'of this suspicious activity.'
    '\n\n'
    'If this email was sent in error, you can still send '
    'the thank you email by using this link.'
)

# text body for warning completed different transaction email.
completed_different_transaction = (
    'This is a message to inform you that a recent Paypal '
    'transaction was made and the transaction id is a '
    'duplicate of an existing completed transaction.\n\n'
    'This could mean that a fraudster has reused an old, '
    'completed transaction.'
    '\n\n'
    'The automatic thank you email was not sent because '
    'of this suspicious activity.'
    '\n\n'
    'If this email was sent in error, you can still send '
    'the thank you email by using this link.'
)

# text body for warning validate amount email.
validate_amount = (
    'This is a message to inform you that a recent Paypal '
    'transaction was made and the amount paid was not one of the fixed '
    'amount on the donations page. This activity is flagged as '
    'suspicious because the payer did not select \'Other\' to donate a '
    'custom amount and their payment amount did not fall within '
    'these fixed amounts {0}.\n'
    'This could mean that someone mingled with the HTML of the '
    'donation page to set another amount.'
    '\n\n'
    'The automatic thank you email was not sent because '
    'of this suspicious activity.'
    '\n\n'
    'If this email was sent in error, you can still send '
    'the thank you email by using this link.'
)

ipn_info_warning_email = (
    '\n\n\n'
    'TRANSACTION DETAILS\n'
    'transaction id: {0}'
    '\n'
    'receiver email: {1}'
    '\n'
    'payer email: {2}'
    '\n'
    'payer full name: {3} {4}'
    '\n'
    'payment status: {5}'
    '\n'
    'payment date: {6}'
    '\n'
    'item name: {7}'
    '\n'
    'item number: {8}'
    '\n'
    'option selected: {9}'
    '\n'
    'payment gross: {10}'
    '\n'
    'currency: {11}'
    '\n'
    'mc gross (same as payment gross if currency is USD): {12}'
)
