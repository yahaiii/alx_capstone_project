from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length

class TransactionForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()], format='%Y-%m-%d')
    cashflow = SelectField('Cashflow', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[InputRequired()])
    category = category = SelectField('Category', coerce=int)
    mode = StringField('Mode', validators=[InputRequired(), Length(max=50)])
    comment = TextAreaField('Comment', validators=[Length(max=255)])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Transaction')


    # Add more custom validation methods if needed

