from datetime import datetime

from .database import db


class IPN(db.Model):
    __tablename__ = 'IPN'

    txn_id = db.Column(db.String(25), primary_key=True)
    receiver_email = db.Column(db.String(80))
    payer_email = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    payment_status = db.Column(db.String(25))
    payment_date = db.Column(db.String(80))
    item_name = db.Column(db.String(150))
    item_number = db.Column(db.String(150))
    option_selection1 = db.Column(db.String(20))
    payment_gross = db.Column(db.Float)
    payment_fee = db.Column(db.Float)
    mc_gross = db.Column(db.Float)
    mc_fee = db.Column(db.Float)
    mc_currency = db.Column(db.String(10))
    memo = db.Column(db.String(255))
    created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    modified = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(
        self, txn_id, receiver_email, payer_email,
        first_name, last_name, payment_status, payment_date,
        item_name, item_number, option_selection1,
        payment_gross, payment_fee,
        mc_gross, mc_fee, mc_currency, memo
    ):
        self.txn_id = txn_id
        self.receiver_email = receiver_email
        self.payer_email = payer_email
        self.first_name = first_name
        self.last_name = last_name
        self.payment_status = payment_status
        self.payment_date = payment_date
        self.item_name = item_name
        self.item_number = item_number
        self.option_selection1 = option_selection1
        self.payment_gross = payment_gross
        self.payment_fee = payment_fee
        self.mc_gross = mc_gross
        self.mc_fee = mc_fee
        self.mc_currency = mc_currency
        self.memo = memo

    def __repr__(self):
        return '<IPN {}>'.format(self.txn_id)

    def payment_net(self):
        return float(self.payment_gross - self.payment_fee)
