from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField, TextAreaField, FloatField, PasswordField, DecimalField, SelectField, DateField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
import shelve


class Tempform(FlaskForm):
    nric = StringField("nric", validators=[DataRequired(),Length(min=4, max=4)])
    temperature = FloatField("Temperature", validators=[DataRequired()])
    symptoms = RadioField("Symptoms", validators=[DataRequired()], choices=[('yes','Yes'), ('no', 'No')])
    contact = RadioField("Contact", validators=[DataRequired()], choices=[('yes','Yes'), ('no', 'No')])
    check = BooleanField("I hereby declare that I have answered the above questions truthfully. I understand that a false declaration is equivalent to an attempt to wilfully deceive Singapore Government officials and cause harm to public safety, and that I may be prosecuted for such offences.", validators=[DataRequired()])
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

class SearchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField('search')

class ProductForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    info = StringField("info", validators=[DataRequired()])
    price = DecimalField("price", validators=[DataRequired()])
    submit = SubmitField("Add")

class PriceForm(FlaskForm):
    price = DecimalField('price', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class ControlForm(FlaskForm):
    add = SubmitField('Add')
    remove = SubmitField('Remove')

class ResetForm(FlaskForm):
    reset = SubmitField("Reset all")

class TimeForm(FlaskForm):
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d')
    time1 = DateTimeField('time1', validators=[DataRequired()], format='%H:%M')
    time2 = DateTimeField('time2', validators=[DataRequired()], format='%H:%M')
    search = SubmitField('Search')
    

class UpdateForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    info = StringField("info", validators=[DataRequired()])
    price = DecimalField("price", validators=[DataRequired()])
    submit = SubmitField("Update")

class CartForm(FlaskForm):
    quantity = IntegerField("quantity", validators=[DataRequired()])
    submit = SubmitField("add")

class DiscountForm(FlaskForm):
    code = StringField("code", validators=[DataRequired()])
    submit = SubmitField("Apply")