from flask import Blueprint, get_flashed_messages, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app.forms.registration_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for a new user. It receives a POST request with the user's registration details and creates a new user account if the provided information is valid. If the registration is successful, the user is redirected to the login page. If there are validation errors or if the username or email is already taken, appropriate error messages are flashed and the registration form is rendered again.

    Parameters:
    - None

    Returns:
    - If the registration is successful, the function redirects to the login page.
    - If there are validation errors or if the username or email is already taken, the registration form is rendered again.

    """
    form = RegistrationForm()

    if form.validate_on_submit():
        # Form submission
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        # Check if the username and email are unique
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash('This username is already taken. Please choose a different one.', 'danger')
        elif existing_email:
            flash('An account with this email already exists. Please use a different email address.', 'danger')
        else:
            # Create a new user and set the password
            new_user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('registration.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm

    print("Debug: Form created")

    if form.validate_on_submit():

        print("Debug: Form submitted check passed")
        # Form submission
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("Debug: Invalid username or password")
            flash('Invalid username or password', 'danger')
            print("Debug: Flash message set")
            return redirect(url_for('auth.login'))

        login_user(user)  # Log the user in

        # Redirect to the 'next' page if provided, or to a default page
        next_page = request.args.get('next')
        print("Debug: Flash messages:", get_flashed_messages())  # Add this print
        return redirect(next_page or url_for('landing.landing_page'))

    return render_template('login.html', form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))