from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, DecimalField, ValidationError
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo

class AccountSettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

class ProfileSettingsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')

class SetGoalsForm(FlaskForm):
    spending_limit = DecimalField('Spending Limit', places=2, validators=[InputRequired()])
    income_goal = DecimalField('Income Goal', places=2, validators=[InputRequired()])
    submit = SubmitField('Set Goals')

    # Custom validation for the fields, e.g., ensuring positive values
    def validate_spending_limit(form, field):
        if field.data < 0:
            raise ValidationError('Spending limit must be a positive value.')

    def validate_income_goal(form, field):
        if field.data < 0:
            raise ValidationError('Income goal must be a positive value.')
