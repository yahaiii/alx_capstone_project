"""
Renders the landing page template.

Returns:
    The rendered landing.html template.
"""
from flask import Blueprint, render_template

# Create a Blueprint for the landing page routes
landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def landing_page():
    return render_template('landing.html')

# Define other landing page routes as needed
