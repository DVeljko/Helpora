from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Length(max=255), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(max=255)])
    login = SubmitField('Log in')


class RegisterForm(FlaskForm):
    name = StringField('Name ', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Length(min=8), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

class CampaignForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('medical', 'Medical'), ('housing', 'Housing'), ('financial', 'Financial Support')] , validators=[DataRequired()])
    image = FileField('Campaign Image', validators=[FileAllowed(['jpg','jpeg','png','webp'], 'Images only!')])
    goal_amount = FloatField('Goal amount', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DonateForm(FlaskForm):
    amount = FloatField('Amount for donating:', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Donate')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')

class PasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')