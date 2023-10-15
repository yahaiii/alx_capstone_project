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
    # Implement logic for spending vs goal visualizations and income vs expenses visualizations
    # You can use a data visualization library (e.g., Plotly) to create the charts

    # Query transactions and paginate the results
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust the number of items per page as needed
    transactions = Transaction.query.filter_by(user_id=current_user.id).paginate()

    return render_template('dashboard.html', transactions=transactions)

@dashboard_bp.route('/transactions', methods=['GET'])
@login_required
def transaction_history():
    # Retrieve and display the transaction history for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transaction_history.html', transactions=transactions)


# Define additional routes for spending vs. goal and income vs. expenses visualizations here

# Add more routes and views as needed
