from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Transaction, Category
from app.forms.transaction_form import TransactionForm

# Create a Blueprint for the dashboard
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Query transactions for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Calculate total income, total expenses, and account balance
    total_income = sum(transaction.amount for transaction in transactions if transaction.cashflow == 'income')
    total_expenses = sum(transaction.amount for transaction in transactions if transaction.cashflow == 'expense')
    account_balance = total_income - total_expenses

    return render_template('dashboard.html', transactions=transactions, total_income=total_income, total_expenses=total_expenses, account_balance=account_balance)

@dashboard_bp.route('/transactions', methods=['GET'])
@login_required
def transaction_history():
    # Retrieve and display the transaction history for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=transactions)


# Define additional routes for spending vs. goal and income vs. expenses visualizations here

# Add more routes and views as needed
