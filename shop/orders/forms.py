from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Regexp


class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()], render_kw={"placeholder": "Full Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "City"})
    zip_code = StringField('ZIP Code', validators=[DataRequired()], render_kw={"placeholder": "ZIP Code"})
    phone = StringField('Mobile Number', validators=[Regexp(regex=r'^01\d{9}$', message='Enter a valid Egyptian mobile number starting with "01" and consisting of 11 digits')], render_kw={"placeholder": "Phone Number"})
    order_notes = TextAreaField('Order Notes', render_kw={"placeholder": "Order Notes"})
    payment_method = RadioField(
        'Payment Method',
        choices=[('bank_transfer', 'Direct Bank Transfer'), 
                 ('cheque', 'Cheque Payment'), 
                 ('paypal', 'Paypal System')],
        default='bank_transfer'
    )
    submit = SubmitField('Place Your Order')
