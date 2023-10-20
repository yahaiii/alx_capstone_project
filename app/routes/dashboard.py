from flask import Blueprint, render_template, request
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

    # Calculate total expenses for different categories
    expense_categories = {}
    for transaction in transactions:
        if transaction.cashflow == 'expense':
            # Use .name to fetch the category name
            category = transaction.category.name  
            expense_categories[category] = expense_categories.get(category, 0) + transaction.amount

    # Convert expense categories data to a format suitable for Chart.js
    category_labels = list(expense_categories.keys())
    category_values = list(expense_categories.values())

    return render_template('dashboard.html', transactions=transactions, total_income=total_income, total_expenses=total_expenses, category_labels=category_labels, category_values=category_values)

@dashboard_bp.route('/transactions', methods=['GET'])
@login_required
def transaction_history():
    # Retrieve and display the transaction history for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=transactions)
