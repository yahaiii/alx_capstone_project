from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Transaction, Category
from app.forms.transaction_form import TransactionForm

# Create a Blueprint for the transactions routes
transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET'])
@login_required
def transaction_history():
    # Retrieve the flash message from the session if available
    message = flash('success')

    # Retrieve and display the transaction history for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=transactions)

@transactions_bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()

    # Fetch categories from the Category model.
    categories = Category.query.all()

    # Pass the categories to the form.
    form.category.choices = [(category.id, category.name) for category in categories]

    # Query transactions for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Create a dictionary to store the total expenses for each category
    total_expenses = {}
    for category in categories:
        total_expenses[category.name] = sum(transaction.amount for transaction in transactions if transaction.category == category and transaction.cashflow == 'expense')

    # Calculate total income
    total_income = sum(transaction.amount for transaction in transactions if transaction.cashflow == 'income')

    # Calculate total expenses across all categories
    total_expenses_all_categories = sum(expense for category_name, expense in total_expenses.items())

    # Define category_names variable
    category_names = list(total_expenses.keys())

    if form.validate_on_submit():
        # Add the new transaction to the database
        transaction = Transaction(
            date=form.date.data,
            cashflow=form.cashflow.data,
            category_id=form.category.data,
            mode=form.mode.data,
            comment=form.comment.data,
            amount=form.amount.data,
            user=current_user
        )

        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully', 'success')
        return redirect(url_for('transactions.transaction_history'))

    return render_template('add_transaction.html', form=form, total_income=total_income, total_expenses_all_categories=total_expenses_all_categories, transactions=transactions, total_expenses=total_expenses, category_names=category_names)



@transactions_bp.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    # Retrieve the transaction to edit
    transaction = Transaction.query.get_or_404(transaction_id)

    # Check if the current user owns the transaction
    if transaction.user != current_user:
        flash("You don't have permission to edit this transaction.", 'error')
        return redirect(url_for('transactions.transaction_history'))

    form = TransactionForm(request.form, obj=transaction)

    # Fetch categories from the Category model
    categories = Category.query.all()
    category_choices = [(str(category.id), category.name) for category in categories]

    # Set the choices for the category field in the form
    form.category.choices = category_choices

    # Query transactions for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Calculate total income, total expenses, and account balance
    total_income = sum(transaction.amount for transaction in transactions if transaction.cashflow == 'income')
    total_expenses = sum(transaction.amount for transaction in transactions if transaction.cashflow == 'expense')

    if form.validate_on_submit():
        # Manually update the transaction with the new data
        transaction.date = form.date.data
        transaction.cashflow = form.cashflow.data
        transaction.comment = form.comment.data
        transaction.amount = form.amount.data
        transaction.category_id = form.category.data
        transaction.mode = form.mode.data
        
        db.session.commit()
        flash('Transaction updated successfully', 'success')
        return redirect(url_for('transactions.transaction_history'))


    return render_template('edit_transaction.html', form=form, transaction=transaction, total_expenses=total_expenses, total_income=total_income, transactions=transactions)



@transactions_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    # Retrieve the transaction to delete
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Check if the current user owns the transaction
    if transaction.user == current_user:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully', 'success')
    else:
        flash("You don't have permission to delete this transaction.", 'error')
    
    return redirect(url_for('transactions.transaction_history'))
