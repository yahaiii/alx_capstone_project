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
    
    if form.validate_on_submit():
        # Create a new transaction and add it to the database
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
    
    return render_template('add_transaction.html', form=form)

@transactions_bp.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    # Retrieve the transaction to edit
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Check if the current user owns the transaction
    if transaction.user != current_user:
        flash("You don't have permission to edit this transaction.", 'error')
        return redirect(url_for('transactions.transaction_history'))
    
    form = TransactionForm(obj=transaction)
    
    if form.validate_on_submit():
        # Update the transaction with the new data
        form.populate_obj(transaction)
        db.session.commit()
        flash('Transaction updated successfully', 'success')
        return redirect(url_for('transactions.transaction_history'))
    
    return render_template('edit_transaction.html', form=form, transaction=transaction)

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
