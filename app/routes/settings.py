from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.forms.settings_form import ProfileSettingsForm, AccountSettingsForm, ChangePasswordForm, SetGoalsForm
from app.models import db

# Create a Blueprint for the user settings routes
settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    # Create forms for profile settings, account settings, change password, and set goals
    profile_form = ProfileSettingsForm()
    account_form = AccountSettingsForm()
    password_form = ChangePasswordForm()
    goals_form = SetGoalsForm()

    if request.method == 'POST':
        if profile_form.validate_on_submit():
            # Handle profile settings update, e.g., update first name, last name, and date of birth
            current_user.first_name = profile_form.first_name.data
            current_user.last_name = profile_form.last_name.data
            current_user.date_of_birth = profile_form.date_of_birth.data
            # Save the changes to the database
            db.session.commit()
            flash('Profile settings updated successfully.', 'success')

        elif account_form.validate_on_submit():
            # Handle account settings update, e.g., update username and email
            current_user.username = account_form.username.data
            current_user.email = account_form.email.data
            # Save the changes to the database
            db.session.commit()
            flash('Account settings updated successfully.', 'success')

        elif password_form.validate_on_submit():
            # Handle password change
            new_password = password_form.new_password.data
            # Check if the current password authorizes the change
            if current_user.check_password(password_form.current_password.data):
                # Update the user's password
                current_user.set_password(new_password)
                # Save the changes to the database
                db.session.commit()
                flash('Password changed successfully.', 'success')
            else:
                flash('Current password is incorrect. Password not changed.', 'danger')

        elif goals_form.validate_on_submit():
            # Handle setting goals, e.g., spending limit and income goal
            current_user.spending_limit = goals_form.spending_limit.data
            current_user.income_goal = goals_form.income_goal.data
            # Save the changes to the database
            db.session.commit()
            flash('Goals set successfully.', 'success')

    return render_template('user_settings.html', profile_form=profile_form, account_form=account_form, password_form=password_form, goals_form=goals_form)
