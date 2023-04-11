from wtforms import Form, StringField, PasswordField, validators,SubmitField,ValidationError
from flask_wtf.file import FileRequired,FileAllowed,FileField
from flask_wtf import FlaskForm
from .models import Customer


class CustomerRegistration(FlaskForm):
    name=StringField('Name :')
    username=StringField('Username :',[validators.DataRequired()])
    email=StringField('Email :', [validators.Email(),validators.DataRequired()])
    password=PasswordField('Password :', [validators.DataRequired(),validators.EqualTo('confirm',message='Both passwords must match')])
    confirm=PasswordField('Confirm Password :',[validators.DataRequired()]) 
    
    phoneno=StringField('Phone No :',[validators.DataRequired()])
    country=StringField('Country :',[validators.DataRequired()])
    state=StringField('State :',[validators.DataRequired()])
    city=StringField('City :',[validators.DataRequired()])
    address=StringField('Address :',[validators.DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
         if Customer.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already taken!")
            
    def validate_email(self, email):
         if Customer.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already taken!")

class CustomerLogin(FlaskForm):
    email=StringField('Email :', [validators.Email(),validators.DataRequired()])
    password=PasswordField('Password :', [validators.DataRequired()])