# app/routes.py

from flask import Blueprint, render_template

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    """
    Index route.
    Displays a welcome message.
    """
    return "<h1>Hello, World! Your Flask App is Running!</h1>"