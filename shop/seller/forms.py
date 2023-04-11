from wtforms import Form, StringField, PasswordField, validators,SubmitField,ValidationError,TextAreaField
from flask_wtf.file import FileRequired,FileAllowed,FileField
from flask_wtf import FlaskForm
from .models import Seller


class SellerRegistration(Form):
    name=StringField('Name :')
    email=StringField('Email :', [validators.Email(),validators.DataRequired()])
    password=PasswordField('Password :', [validators.DataRequired(),validators.EqualTo('confirm',message='Both passwords must match')])
    confirm=PasswordField('Confirm Password :',[validators.DataRequired()]) 
    
    phoneno=StringField('Phone No :',[validators.DataRequired()])
    address=TextAreaField('Address :',[validators.DataRequired()])

    gst_no=StringField('GST Number :',[validators.DataRequired()])
    pan_no=StringField('Pan Card :',[validators.DataRequired()])
    submit = SubmitField('Register')
            
    def validate_email(self, email):
         if Seller.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already taken!")


class SellerLogin(Form):
    email=StringField('Email :', [validators.Email(),validators.DataRequired()])
    password=PasswordField('Password :', [validators.DataRequired()])