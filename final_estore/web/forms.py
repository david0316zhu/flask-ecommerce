from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import shelve


class Tempform(FlaskForm):
    nric = TextAreaField("nric", validators=[DataRequired(),Length(min=4, max=4)])
    temperature = FloatField("Temperature", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


