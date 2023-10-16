from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length

class TransactionForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()], format='%Y-%m-%d')
    cashflow = SelectField('Cashflow', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[InputRequired()])
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    mode = SelectField('Mode', choices=[
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('Mobile', 'Mobile Money')
        # ... Other modes
        ], validators=[InputRequired()])
    comment = TextAreaField('Comment', validators=[Length(max=255)])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Transaction')


    # Add more custom validation methods if needed

