from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from greenlife.models import User, Service, ServiceType, DurationOptions
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a diffrent one')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a diffrent one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a diffrent one')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a diffrent one')
            
class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=120)])
    service_type = SelectField('Type', validators=[DataRequired()])
    duration = SelectField('Duration', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()]) 
    submit = SubmitField('Create Service')

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.service_type.choices = (('','-- select --'),) + tuple(
            [(st.id, st.name) for st in ServiceType.query.all()]
        )
        self.duration.choices = (('', '-- select --'),) + tuple(
            [(do.id, do.name) for do in DurationOptions.query.all()]
        )

    original_name = None
    original_description = None
    original_service_type = None
    original_duration = None
    original_price = None

    def validate_name(self, name):
        if name.data != self.original_name:
            service_name = Service.query.filter_by(name=name.data).first()
            if service_name:
                raise ValidationError('This name is already taken, use a diffrent one')
    
    def is_updated(self, name, description, service_type, duration, price):
        return (
            name.data == self.original_name and
            description.data == self.original_description and 
            int(service_type.data) == self.original_service_type and 
            int(duration.data) == self.original_duration and 
            Decimal(price.data) == Decimal(self.original_price)
        )
    
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. you must register first.')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# class AppointmentForm(FlaskForm):

# class MessageForm(FlaskForm):

# class QueryForm(FlaskForm):

