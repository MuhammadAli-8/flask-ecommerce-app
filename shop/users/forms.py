from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, Optional
from shop.models import User
from flask_login import current_user


class RegisterationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Mobile Number', validators=[Regexp(regex=r'^01\d{9}$', message='Enter a valid Egyptian mobile number starting with "01" and consisting of 11 digits')])
    address = StringField('Enter Your Full Address', validators=[Length(min=10, max=300)])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That Email is taken. Please choose a different one.')

    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateInformationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Mobile Number', validators=[DataRequired(), Regexp(regex=r'^01\d{9}$', message='Enter a valid Egyptian mobile number starting with "01" and consisting of 11 digits')])
    address = StringField('Enter Your Full Address', validators=[DataRequired(), Length(min=10, max=300)])
    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
