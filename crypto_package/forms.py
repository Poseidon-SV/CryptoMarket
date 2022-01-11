# from re import U
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from crypto_package.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check): #(FlaskForm) auto checks the field with name validate and then realtion which is here username, It's all depends on nomenclatuer
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('This Username is already taken!! Please try a different username')
    def validate_email(self, email_to_check): #(FlaskForm) auto checks the field with name validate and then realtion which is here username, It's all depends on nomenclatuer
        email = User.query.filter_by(email = email_to_check.data).first()
        if email:
            raise ValidationError('This Email is already in use!! Please try a different email')

    username = StringField(label='User Name', validators= [Length(min = 5, max= 30), DataRequired()])
    email = EmailField(label="Email Address") 
    password1 = PasswordField(label='Password', validators= [Length(min=  6), DataRequired()])
    password2 = PasswordField(label= 'Confirm Password', validators= [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label= 'Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators= [DataRequired()])
    password = PasswordField(label='Password', validators= [DataRequired()])
    submit = SubmitField(label= 'Login')

class PurchaseCurrencyForm(FlaskForm):
    submit = SubmitField(label= 'Buy')

class SellCurrencyForm(FlaskForm):
    submit = SubmitField(label= 'Sell')