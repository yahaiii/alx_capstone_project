from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.forms.settings_form import ProfileSettingsForm, AccountSettingsForm, ChangePasswordForm, SetGoalsForm, SpendingLimitsForm
from app.models import Category, db, Goal

# Create a Blueprint for the user settings routes
settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():

    
    
    # Create forms for profile settings, account settings, change password, and set goals
    profile_form = ProfileSettingsForm(obj=current_user)  # Prefill with user data
    account_form = AccountSettingsForm(obj=current_user)  # Prefill with user data
    password_form = ChangePasswordForm()
    goals_form = SetGoalsForm(obj=current_user)  # Prefill with user data
    spending_limits_form = SpendingLimitsForm(obj=current_user)  # Prefill with user data

    # Fetch categories from the database
    categories = Category.query.all()

     # Dynamically set the choices for the category field
    spending_limits_form.category.choices = [(category.id, category.name) for category in categories]



    if request.method == 'POST':
        if profile_form.validate_on_submit():
            # Handle profile settings update
            profile_form.populate_obj(current_user)
            db.session.commit()
            flash('Profile settings updated successfully.', 'success')

        if account_form.validate_on_submit():
            # Handle account settings update
            account_form.populate_obj(current_user)
            db.session.commit()
            flash('Account settings updated successfully.', 'success')

        if password_form.validate_on_submit():
            # Handle password change
            new_password = password_form.new_password.data
            # Check if the current password authorizes the change
            if current_user.check_password(password_form.current_password.data):
                current_user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully.', 'success')
            else:
                flash('Current password is incorrect. Password not changed.', 'danger')
        
        if spending_limits_form.validate_on_submit():
            # Get the selected category and spending limit from the form
            selected_category_id = spending_limits_form.category.data
            new_spending_limit = spending_limits_form.spending_limit.data

            # Find the category object based on the selected_category_id
            selected_category = Category.query.get(selected_category_id)

            if selected_category:
                # Update the spending limit for the selected category
                selected_category.spending_limit = new_spending_limit
                db.session.commit()
                flash('Spending limits updated successfully.', 'success')
            else:
                flash('Category not found. Spending limits not updated.', 'danger')


    return render_template('settings.html', profile_form=profile_form, account_form=account_form, password_form=password_form, goals_form=goals_form, spending_limits_form=spending_limits_form, categories=categories)
