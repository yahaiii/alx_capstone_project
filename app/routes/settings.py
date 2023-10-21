from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.forms.settings_form import ProfileSettingsForm, AccountSettingsForm, ChangePasswordForm, SetGoalsForm
from app.models import db, Goal

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

        if goals_form.validate_on_submit():
        # Create a new Goal instance and populate it with the form data
            if goals_form.validate_on_submit():
                name = goals_form.name.data
                goal_type = goals_form.goal_type.data
                target_amount = goals_form.target_amount.data
                user_id = current_user.id  # Assuming user ID is associated with the goal

                goal = Goal(name=name, goal_type=goal_type, target_amount=target_amount, user_id=user_id)
                db.session.add(goal)
                db.session.commit()
                flash('Goal set successfully.', 'success')

    return render_template('settings.html', profile_form=profile_form, account_form=account_form, password_form=password_form, goals_form=goals_form)
